// Lyric Programming Language
// Copyright (c) 2025-2026 MiraNova Studio
// All rights reserved.

using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Win32;

class PythonCmd
{
    public string File;
    public string Prefix;
    public string Display;
}

class LyricSetup
{
    static Label _status;
    static ProgressBar _meter;
    static System.Windows.Forms.Timer _meterTimer;
    static int _meterTarget;

    [STAThread]
    static void Main(string[] args)
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);

        bool uninstall = false;
        bool quiet = false;
        if (args != null)
        {
            foreach (string arg in args)
            {
                if (string.Equals(arg, "/uninstall", StringComparison.OrdinalIgnoreCase)) uninstall = true;
                if (string.Equals(arg, "/quiet", StringComparison.OrdinalIgnoreCase)) quiet = true;
            }
        }

        if (uninstall)
        {
#if BUNDLED
            UninstallBundled(quiet);
#else
            UninstallExisting(quiet);
#endif
            return;
        }

#if BUNDLED
        if (!Confirm("Install Lyric and the copy of Python included in this setup?\r\n\r\nPython is installed only for Lyric. A Python already on this PC is left as it is."))
            return;
        InstallBundled();
#else
        PythonCmd python = FindPython();
        if (python == null)
        {
            MessageBox.Show(
                "Python 3.10 or newer is not installed.\r\n\r\nInstall Python, then run this setup again.",
                "Lyric Setup",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error,
                MessageBoxDefaultButton.Button1,
                MessageBoxOptions.DefaultDesktopOnly);
            return;
        }
        if (!Confirm("Install Lyric into the Python already on this PC?"))
            return;
        InstallIntoExistingPython(python);
#endif
    }

    static Icon _appIcon;

    static Icon AppIcon()
    {
        if (_appIcon == null)
            _appIcon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);
        return _appIcon;
    }

    static DialogResult ShowMessage(string text, MessageBoxButtons buttons, MessageBoxIcon icon)
    {
        using (Form owner = new Form())
        {
            owner.ShowInTaskbar = false;
            try
            {
                if (owner.Handle != IntPtr.Zero)
                    owner.Icon = AppIcon();
            }
            catch (Exception)
            {
            }
            return MessageBox.Show(owner, text, "Lyric Setup", buttons, icon);
        }
    }

    static bool Confirm(string text)
    {
        return ShowMessage(text, MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes;
    }

    static void InstallIntoExistingPython(PythonCmd python)
    {
        ShowStatus("Installing Lyric into\r\n" + python.Display);
        SetProgress("Installing Lyric into\r\n" + python.Display, 92);
        string wheel = ExtractResource("lyric.whl", WheelInfo.FileName);
        string output;
        int code = Run(python.File, Join(python.Prefix, "-m pip install --upgrade --no-deps \"" + wheel + "\""), null, out output);
        TryDelete(wheel);
        if (code == 0) FillProgress();
        CloseStatus();
        if (code == 0)
            RegisterInstalled(python.Display, python.File, python.Prefix);
        Finish(code, output, "Lyric is installed.\r\n\r\nOpen a new terminal and run:\r\nlyric --version\r\n\r\nRemove it later from Installed apps.");
    }

    static void UninstallExisting(bool quiet)
    {
        if (!quiet && !Confirm("Remove Lyric from this PC?"))
            return;

        string pythonFile = ReadUninstallValue("PythonFile");
        string pythonPrefix = ReadUninstallValue("PythonPrefix");
        if (string.IsNullOrEmpty(pythonFile))
        {
            PythonCmd python = FindPython();
            if (python != null)
            {
                pythonFile = python.File;
                pythonPrefix = python.Prefix;
            }
        }

        int code = 0;
        string output = "";
        if (!string.IsNullOrEmpty(pythonFile))
        {
            ShowStatus("Removing Lyric...");
            SetProgress("Removing Lyric...", 90);
            code = Run(pythonFile, Join(pythonPrefix, "-m pip uninstall -y lyric-lang"), null, out output);
            if (code == 0) FillProgress();
            CloseStatus();
        }

        if (code != 0)
        {
            if (!quiet)
                Finish(code, output, "");
            return;
        }

        ScheduleDelete(UninstallerDir());
        if (!quiet)
            ShowMessage("Lyric is removed.", MessageBoxButtons.OK, MessageBoxIcon.Information);
    }

#if BUNDLED
    static void InstallBundled()
    {
        string installDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "Programs",
            "Lyric");
        ShowStatus("Installing Lyric and Python into\r\n" + installDir);

        string zip = ExtractResource("python.zip", "python-embed.zip");
        string getPip = ExtractResource("getpip.py", "get-pip.py");
        string wheel = ExtractResource("lyric.whl", WheelInfo.FileName);
        string output = "";
        int code = 0;
        try
        {
            Directory.CreateDirectory(installDir);
            SetProgress("Extracting Python...", 32);
            code = Run(Path.Combine(Environment.SystemDirectory, "tar.exe"), "-xf \"" + zip + "\" -C \"" + installDir + "\"", null, out output);
            if (code != 0)
            {
                Finish(code, output, "");
                return;
            }

            EnableSitePackages(installDir);
            string pythonExe = Path.Combine(installDir, "python.exe");

            SetProgress("Installing pip...", 68);
            code = Run(pythonExe, "\"" + getPip + "\" --no-warn-script-location", installDir, out output);
            if (code != 0)
            {
                Finish(code, output, "");
                return;
            }

            SetProgress("Installing Lyric...", 96);
            code = Run(pythonExe, "-m pip install --upgrade --no-deps --no-warn-script-location \"" + wheel + "\"", installDir, out output);
            if (code != 0)
            {
                Finish(code, output, "");
                return;
            }

            AddToUserPath(Path.Combine(installDir, "Scripts"));
            if (code == 0) FillProgress();
        }
        finally
        {
            TryDelete(zip);
            TryDelete(getPip);
            TryDelete(wheel);
            CloseStatus();
        }

        if (code == 0)
            RegisterInstalled(installDir, "", "");
        Finish(code, output, "Lyric is installed with its own Python.\r\n\r\nOpen a new terminal and run:\r\nlyric --version\r\n\r\nRemove it later from Installed apps.");
    }

    static void UninstallBundled(bool quiet)
    {
        if (!quiet && !Confirm("Remove Lyric and the Python installed for it?"))
            return;

        string installDir = ReadUninstallValue("InstallLocation");
        if (string.IsNullOrEmpty(installDir))
            installDir = BundledInstallDir();
        if (!IsBundledInstallDir(installDir))
        {
            if (!quiet)
                ShowMessage("The Lyric install folder was not found.", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        RemoveFromUserPath(Path.Combine(installDir, "Scripts"));
        ScheduleDelete(installDir);
        if (!quiet)
            ShowMessage("Lyric is removed.", MessageBoxButtons.OK, MessageBoxIcon.Information);
    }

    static void EnableSitePackages(string installDir)
    {
        string[] pthFiles = Directory.GetFiles(installDir, "python*._pth");
        if (pthFiles.Length == 0)
            throw new InvalidOperationException("The bundled Python is missing its ._pth file.");

        string zipLine = "python.zip";
        foreach (string line in File.ReadAllLines(pthFiles[0]))
        {
            string trimmed = line.Trim();
            if (trimmed.EndsWith(".zip"))
            {
                zipLine = trimmed;
                break;
            }
        }
        File.WriteAllText(pthFiles[0], zipLine + "\r\n.\r\nLib\\site-packages\r\nimport site\r\n");
    }

    static void AddToUserPath(string directory)
    {
        string current = Environment.GetEnvironmentVariable("Path", EnvironmentVariableTarget.User);
        if (current == null) current = "";
        string[] parts = current.Split(new char[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
        foreach (string part in parts)
        {
            if (string.Equals(part.TrimEnd('\\'), directory.TrimEnd('\\'), StringComparison.OrdinalIgnoreCase))
                return;
        }
        string updated = current.Trim().TrimEnd(';');
        if (updated.Length == 0) updated = directory;
        else updated = updated + ";" + directory;
        Environment.SetEnvironmentVariable("Path", updated, EnvironmentVariableTarget.User);

        IntPtr result;
        SendMessageTimeout(new IntPtr(0xffff), 0x001A, IntPtr.Zero, "Environment", 2, 5000, out result);
    }

    static void RemoveFromUserPath(string directory)
    {
        string current = Environment.GetEnvironmentVariable("Path", EnvironmentVariableTarget.User);
        if (string.IsNullOrEmpty(current)) return;
        string target = directory.Trim().TrimEnd('\\');
        string[] parts = current.Split(new char[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
        string updated = "";
        foreach (string part in parts)
        {
            if (string.Equals(part.Trim().TrimEnd('\\'), target, StringComparison.OrdinalIgnoreCase))
                continue;
            if (updated.Length > 0) updated += ";";
            updated += part.Trim();
        }
        Environment.SetEnvironmentVariable("Path", updated, EnvironmentVariableTarget.User);

        IntPtr result;
        SendMessageTimeout(new IntPtr(0xffff), 0x001A, IntPtr.Zero, "Environment", 2, 5000, out result);
    }

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    static extern IntPtr SendMessageTimeout(IntPtr hWnd, int msg, IntPtr wParam, string lParam, int flags, int timeout, out IntPtr result);
#endif

    static PythonCmd FindPython()
    {
        PythonCmd found = Probe("py", "-3");
        if (found != null) return found;
        found = Probe("python", "");
        if (found != null) return found;
        found = Probe("python3", "");
        if (found != null) return found;

        string[] roots = new string[]
        {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs", "Python"),
            @"C:\Python",
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Python"),
        };
        foreach (string root in roots)
        {
            if (!Directory.Exists(root)) continue;
            string[] files = Directory.GetFiles(root, "python.exe", SearchOption.AllDirectories);
            foreach (string file in files)
            {
                found = Probe(file, "");
                if (found != null) return found;
            }
        }
        return null;
    }

    static PythonCmd Probe(string file, string prefix)
    {
        string resolved = ResolveCommand(file);
        if (resolved == null) return null;
        string output;
        int code;
        try
        {
            code = Run(resolved, Join(prefix, "-c \"import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)\""), null, out output);
        }
        catch (Exception)
        {
            return null;
        }
        if (code != 0) return null;
        return new PythonCmd { File = resolved, Prefix = prefix, Display = resolved };
    }

    static string ResolveCommand(string file)
    {
        if (file.IndexOf('\\') >= 0 || file.IndexOf('/') >= 0 || file.IndexOf(':') >= 0)
        {
            if (IsStoreAlias(file) || !File.Exists(file)) return null;
            return file;
        }

        string pathEnv = Environment.GetEnvironmentVariable("PATH");
        if (string.IsNullOrEmpty(pathEnv)) return null;
        string pathext = Environment.GetEnvironmentVariable("PATHEXT");
        if (string.IsNullOrEmpty(pathext)) pathext = ".EXE;.CMD;.BAT";
        string[] dirs = pathEnv.Split(new char[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
        string[] exts = pathext.Split(new char[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
        foreach (string dir in dirs)
        {
            string trimmed = dir.Trim();
            if (trimmed.Length == 0 || IsStoreAlias(trimmed)) continue;
            string direct = Path.Combine(trimmed, file);
            if (File.Exists(direct) && !IsStoreAlias(direct)) return direct;
            foreach (string ext in exts)
            {
                string candidate = direct + ext;
                if (File.Exists(candidate) && !IsStoreAlias(candidate)) return candidate;
            }
        }
        return null;
    }

    static bool IsStoreAlias(string path)
    {
        return path.IndexOf("\\WindowsApps\\", StringComparison.OrdinalIgnoreCase) >= 0;
    }

    static int Run(string file, string args, string workingDir, out string output)
    {
        ProcessStartInfo info = new ProcessStartInfo();
        info.FileName = file;
        info.Arguments = args;
        info.UseShellExecute = false;
        info.CreateNoWindow = true;
        info.RedirectStandardOutput = true;
        info.RedirectStandardError = true;
        if (!string.IsNullOrEmpty(workingDir))
            info.WorkingDirectory = workingDir;

        using (Process process = Process.Start(info))
        {
            StringBuilder stdout = new StringBuilder();
            StringBuilder stderr = new StringBuilder();
            process.OutputDataReceived += delegate(object sender, DataReceivedEventArgs e)
            {
                if (e.Data == null) return;
                lock (stdout) stdout.AppendLine(e.Data);
            };
            process.ErrorDataReceived += delegate(object sender, DataReceivedEventArgs e)
            {
                if (e.Data == null) return;
                lock (stderr) stderr.AppendLine(e.Data);
            };
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            while (!process.WaitForExit(50))
                Application.DoEvents();
            process.WaitForExit();
            output = stdout.ToString() + stderr.ToString();
            return process.ExitCode;
        }
    }

    static string ExtractResource(string resourceName, string fileName)
    {
        string dest = Path.Combine(Path.GetTempPath(), fileName);
        using (Stream source = Assembly.GetExecutingAssembly().GetManifestResourceStream(resourceName))
        {
            if (source == null)
                throw new InvalidOperationException("Missing installer resource: " + resourceName);
            using (FileStream target = File.Create(dest))
            {
                source.CopyTo(target);
            }
        }
        return dest;
    }

    static void ShowStatus(string text)
    {
        Form form = new Form();
        form.Text = "Lyric Setup";
        form.FormBorderStyle = FormBorderStyle.FixedDialog;
        form.StartPosition = FormStartPosition.CenterScreen;
        form.MaximizeBox = false;
        form.MinimizeBox = false;
        form.Width = 480;
        form.Height = 190;
        form.Icon = AppIcon();
        _status = new Label();
        _status.AutoSize = true;
        _status.Left = 16;
        _status.Top = 24;
        _status.MaximumSize = new System.Drawing.Size(440, 0);
        _status.Text = text;
        form.Controls.Add(_status);
        _meter = new ProgressBar();
        _meter.Left = 16;
        _meter.Top = 100;
        _meter.Width = 440;
        _meter.Height = 18;
        _meter.Minimum = 0;
        _meter.Maximum = 100;
        _meter.Style = ProgressBarStyle.Continuous;
        form.Controls.Add(_meter);
        _meterTarget = 8;
        _meterTimer = new System.Windows.Forms.Timer();
        _meterTimer.Interval = 80;
        _meterTimer.Tick += MeterTick;
        _meterTimer.Start();
        form.Show();
        Application.DoEvents();
    }

    static void MeterTick(object sender, EventArgs e)
    {
        if (_meter == null || _meter.Value >= _meterTarget) return;
        int gap = _meterTarget - _meter.Value;
        int step = 1;
        if (gap > 40) step = 3;
        else if (gap > 15) step = 2;
        int next = _meter.Value + step;
        if (next > _meterTarget) next = _meterTarget;
        SetMeterValue(next);
    }

    static void SetProgress(string text, int target)
    {
        if (target < 0) target = 0;
        if (target > 100) target = 100;
        _meterTarget = target;
        SetStatus(text);
    }

    static void FillProgress()
    {
        _meterTarget = 100;
        SetMeterValue(100);
        Application.DoEvents();
    }

    static void SetMeterValue(int value)
    {
        if (_meter == null) return;
        if (value < 0) value = 0;
        if (value > 100) value = 100;
        if (value > 0)
        {
            _meter.Value = value;
            _meter.Value = value - 1;
        }
        _meter.Value = value;
    }

    static void SetStatus(string text)
    {
        if (_status == null) return;
        _status.Text = text;
        Application.DoEvents();
    }

    static void CloseStatus()
    {
        if (_meterTimer != null)
        {
            _meterTimer.Stop();
            _meterTimer.Tick -= MeterTick;
            _meterTimer.Dispose();
            _meterTimer = null;
        }
        _meter = null;
        if (_status == null) return;
        Form form = _status.FindForm();
        _status = null;
        if (form != null) form.Close();
    }

    static void Finish(int code, string output, string success)
    {
        if (code == 0)
        {
            ShowMessage(success, MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }
        ShowMessage("Install failed.\r\n\r\n" + Tail(output), MessageBoxButtons.OK, MessageBoxIcon.Error);
    }

    static void TryDelete(string path)
    {
        try { if (path != null) File.Delete(path); } catch (Exception) { }
    }

    static string Join(string prefix, string rest)
    {
        if (string.IsNullOrEmpty(prefix)) return rest;
        return prefix + " " + rest;
    }

    static string Tail(string text)
    {
        if (string.IsNullOrEmpty(text)) return "The installer did not report an error.";
        if (text.Length <= 1200) return text;
        return text.Substring(text.Length - 1200);
    }

    static string ProgramsDir()
    {
        return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Programs");
    }

    static string BundledInstallDir()
    {
        return Path.Combine(ProgramsDir(), "Lyric");
    }

    static string UninstallerDir()
    {
#if BUNDLED
        return BundledInstallDir();
#else
        return Path.Combine(ProgramsDir(), "Lyric Setup");
#endif
    }

    static string UninstallKeyPath()
    {
#if BUNDLED
        return @"Software\Microsoft\Windows\CurrentVersion\Uninstall\LyricBundled";
#else
        return @"Software\Microsoft\Windows\CurrentVersion\Uninstall\Lyric";
#endif
    }

    static void RegisterInstalled(string installLocation, string pythonFile, string pythonPrefix)
    {
        string uninstallExe = Path.Combine(UninstallerDir(), "Uninstall.exe");
        try
        {
            Directory.CreateDirectory(UninstallerDir());
            string source = Application.ExecutablePath;
            if (!string.Equals(Path.GetFullPath(source), Path.GetFullPath(uninstallExe), StringComparison.OrdinalIgnoreCase))
                File.Copy(source, uninstallExe, true);
        }
        catch (Exception)
        {
            if (!File.Exists(uninstallExe))
                uninstallExe = Application.ExecutablePath;
        }

        Version version = Assembly.GetExecutingAssembly().GetName().Version;
        string displayVersion = version.Major + "." + version.Minor + "." + version.Build;
        using (RegistryKey key = Registry.CurrentUser.CreateSubKey(UninstallKeyPath()))
        {
            key.SetValue("DisplayName", "Lyric");
            key.SetValue("DisplayVersion", displayVersion);
            key.SetValue("Publisher", "MiraNova Studio");
            key.SetValue("InstallLocation", installLocation);
            key.SetValue("DisplayIcon", uninstallExe);
            key.SetValue("UninstallString", "\"" + uninstallExe + "\" /uninstall");
            key.SetValue("QuietUninstallString", "\"" + uninstallExe + "\" /uninstall /quiet");
            key.SetValue("NoModify", 1, RegistryValueKind.DWord);
            key.SetValue("NoRepair", 1, RegistryValueKind.DWord);
            key.SetValue("EstimatedSize", FolderSizeKb(installLocation), RegistryValueKind.DWord);
            key.SetValue("InstallDate", DateTime.Now.ToString("yyyyMMdd"));
            key.SetValue("URLInfoAbout", "https://github.com/MiraNovaStudio/lyric");
            if (!string.IsNullOrEmpty(pythonFile))
                key.SetValue("PythonFile", pythonFile);
            if (!string.IsNullOrEmpty(pythonPrefix))
                key.SetValue("PythonPrefix", pythonPrefix);
        }
    }

    static int FolderSizeKb(string directory)
    {
        long bytes = 0;
        try
        {
            foreach (string file in Directory.GetFiles(directory, "*", SearchOption.AllDirectories))
            {
                try { bytes += new FileInfo(file).Length; }
                catch (Exception) { }
            }
        }
        catch (Exception)
        {
        }
        int kb = (int)(bytes / 1024);
        if (kb < 1) kb = 1;
        return kb;
    }

    static string ReadUninstallValue(string name)
    {
        using (RegistryKey key = Registry.CurrentUser.OpenSubKey(UninstallKeyPath()))
        {
            if (key == null) return "";
            object value = key.GetValue(name);
            return value == null ? "" : value.ToString();
        }
    }

    static void RemoveRegistration()
    {
        try
        {
            Registry.CurrentUser.DeleteSubKeyTree(UninstallKeyPath(), false);
        }
        catch (Exception)
        {
        }
    }

    static bool IsBundledInstallDir(string directory)
    {
        if (string.IsNullOrEmpty(directory)) return false;
        string full = Path.GetFullPath(directory).TrimEnd('\\');
        string expected = Path.GetFullPath(BundledInstallDir()).TrimEnd('\\');
        return string.Equals(full, expected, StringComparison.OrdinalIgnoreCase);
    }

    static void ScheduleDelete(string directory)
    {
        if (!Directory.Exists(directory))
        {
            RemoveRegistration();
            return;
        }

        string key = "HKCU\\" + UninstallKeyPath();
        ProcessStartInfo info = new ProcessStartInfo();
        info.FileName = "cmd.exe";
        info.Arguments = "/c ping 127.0.0.1 -n 3 >nul & rmdir /s /q \"" + directory + "\" && reg delete \"" + key + "\" /f";
        info.UseShellExecute = false;
        info.CreateNoWindow = true;
        Process.Start(info);
    }
}

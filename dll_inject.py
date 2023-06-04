import random
import sys
from ctypes import *
from win32com.client import GetObject
import colorama
import psutil

def get_process_id_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def generate_random_string(length: int = 20):
    special_chars = "{}@~:?>#|<_-=+/"
    return ''.join(random.choice(special_chars) for _ in range(length))

print(f"{colorama.Fore.LIGHTGREEN_EX}{generate_random_string()}")
print(f"{colorama.Fore.LIGHTCYAN_EX}Ector")
print(f"{colorama.Fore.LIGHTGREEN_EX}{generate_random_string()}")


PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM = ( 0x1000 | 0x2000 )
kernel32 = windll.kernel32

targetProcName = input(f"{colorama.Fore.LIGHTRED_EX}[!] Please Input the target name (e.g: hl2.exe): ")
dll_path = input(f"{colorama.Fore.LIGHTRED_EX}[!] Please Input the target dll (e.g: C:\\test\\Test.DLL): ")
dll_len = len(dll_path)

pid = get_process_id_by_name(str(targetProcName))

if pid == None:
    input(f"{colorama.Fore.LIGHTRED_EX}[!] Error trying to get PID. Make sure you entered the proccess name correctly and make sure it is running.")

# Get handle to process being injected...
h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )

if not h_process:
    input(f"{colorama.Fore.LIGHTRED_EX}[!] Couldn't get handle to PID: %s" %(pid))
    sys.exit(0)

# Allocate space for DLL path
arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

# Write DLL path to allocated space
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

# Resolve LoadLibraryA Address
h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

# Now we createRemoteThread with entrypoiny set to LoadLibraryA and pointer to DLL path as param
thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
    input(f"{colorama.Fore.LIGHTRED_EX}[!] Failed to inject DLL, exit...")
    sys.exit(0)

input(f"{colorama.Fore.LIGHTGREEN_EX}[+] Remote Thread with ID 0x%08x created." %(thread_id.value))

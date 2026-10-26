import ctypes
import sys

# Load Digilent Adept Runtime DLLs
try:
    dmgr = ctypes.CDLL("dmgr.dll")
    dpti = ctypes.CDLL("dpti.dll")
except OSError:
    print("[ERROR] Could not load Adept DLLs.")
    sys.exit(1)

hif = ctypes.c_void_p()
dev_name = b"Genesys2"
port_num = 1  # Synchronous DPTI port

print("[INFO] Opening DPTI connection...")
if not dmgr.DmgrOpen(ctypes.byref(hif), dev_name):
    print("[ERROR] Failed to open device.")
    sys.exit(1)

if not dpti.DptiEnableEx(hif, port_num):
    print("[ERROR] Failed to enable DPTI port.")
    dmgr.DmgrClose(hif)
    sys.exit(1)

# 12 Bytes Payload (Coordinates x and c)
payload = bytearray([
    0x00, 0x3E,  # x[0] = 1.5
    0x00, 0x41,  # x[1] = 2.5
    0x00, 0x38,  # x[2] = 0.5
    0x00, 0x38,  # c[0] = 0.5
    0x00, 0x38,  # c[1] = 0.5
    0x00, 0x38   # c[2] = 0.5
])

c_out = (ctypes.c_ubyte * len(payload))(*payload)
cb_out = ctypes.c_ulong(len(payload))

# Buffer to receive the 2-byte FP16 result back from the FPGA
c_in = (ctypes.c_ubyte * 2)()
cb_in = ctypes.c_ulong(2)

print("[INFO] Streaming coordinates to FPGA and waiting for result...")

# DptiIO handles simultaneous write (12 bytes) and read (2 bytes)
success = dpti.DptiIO(hif, c_out, cb_out, c_in, cb_in, False)

if success:
    res_hex = "".join(format(b, '02x') for b in c_in)
    print(f"[SUCCESS] Received 3D Distance FP16 Result from FPGA: 16'h{res_hex}")
else:
    print("[ERROR] DptiIO transfer failed.")

dpti.DptiDisable(hif)
dmgr.DmgrClose(hif)
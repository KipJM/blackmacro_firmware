from micropython import const
from os import urandom

from blackmacro_lib.modules.module_base import SpeedEditorModule


# micropython doesn't support enums or switch :(

## These two helper methods are only used for testing
def hex_to_bytes(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string.replace(':',''))

# Actual auth data is 8 bytes (64bits), the first two bytes are for auth stages control
def bytes_to_auth_int(auth_bytes: bytes):
    return int.from_bytes(auth_bytes[2:], "little") # strips first 2 bytes


# Adapted from https://github.com/smunaut/blackmagic-misc

# Shift left by 8 bytes (least significant byte -> most significant)
# aka rotate one byte to the right (looped)
def rol8(v):
    return ((v << 56) | (v >> 8)) & 0xffffffffffffffff

# rotate right by n-1 bytes
def rol8n(v, n):
    for i in range(n):
        v = rol8(v)
    return v

# We are checking if davinci is legit. Feel fre
def pc_solve_challenge(challenge: int) -> int:
    """
    Solve the challenge sent from the keyboard, to be solved by PC
    From https://github.com/smunaut/blackmagic-misc
    :param challenge: unencrypted challenge uint64 (no control bytes)
    :return: encrypted uint64 (no control bytes)
    """
    AUTH_EVEN_TBL = [
        0x3ae1206f97c10bc8,
        0x2a9ab32bebf244c6,
        0x20a6f8b8df9adf0a,
        0xaf80ece52cfc1719,
        0xec2ee2f7414fd151,
        0xb055adfd73344a15,
        0xa63d2e3059001187,
        0x751bf623f42e0dde,
    ]
    AUTH_ODD_TBL = [
        0x3e22b34f502e7fde,
        0x24656b981875ab1c,
        0xa17f3456df7bf8c3,
        0x6df72e1941aef698,
        0x72226f011e66ab94,
        0x3831a3c606296b42,
        0xfd7ff81881332c89,
        0x61a3f6474ff236c6,
    ]
    MASK = 0xa79a63f585d37bf0 # 1010011110011010011000111111010110000101110100110111101111110000

    n = challenge & 7 #[0,7]
    # Example
    # a5       98       91       4c       81       44       00       4d
    # 10100101 10011000 10010001 01001100 10000001 01000100 00000000 01001101
    # 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000111
    # 														      => 5


    # Rotate right by 0-7 bytes
    v = rol8n(challenge, n)

    # Example
    # a5       98       91       4c       81       44       00       4d       (n=5, rotate by 4 bytes)
    # 10100101 10011000 10010001 01001100 10000001 01000100 00000000 01001101
    # =>
    # 4c       81       44       00       4d       a5       98       91
    # 01001100 10000001 01000100 00000000 01001101 10100101 10011000 10010001


    # last bit      #01111000, last bit. N: [3-6]: 1, else: 0.
    if (v & 1) == ((0x78 >> n) & 1):
        k = AUTH_EVEN_TBL[n]
    else:
        v = v ^ rol8(v) # XOR rolled, why??
        k = AUTH_ODD_TBL[n]

    return v ^ (rol8(v) & MASK) ^ k

def kbd_solve_challenge(challenge: int) -> int:
    """
    Solve the challenge sent from the PC, to be solved by Speed editor keyboard
    Reverse engineered by me. See editor_key_cracking.ipynb on how the keys are calculated.
    :param challenge: unencrypted challenge uint64 (no control bytes)
    :return: encrypted uint64 (no control bytes)
    """
    AUTH_EVEN_TBL = [
          0x6d82d2aba84359,
        0x8094f1e1139a3aa6,
        0x2d3929003020a05c,
        0xd48c2ddea1133a4f,
        0xd654c05c5fd009d6,
        0x4c6fb9a3fd2862e5,
        0x6fd43b58528cba05,
        0xdce7a14a8971b6de
    ]
    AUTH_ODD_TBL = [
        0x0000000000000000, # Impossible to reach
        0x655ab52052b84a3d,
        0x3142691fe0314ad4,
        0xca2f80438fc1e35e,
        0x52cc143ed3fabbf4,
        0xeb4cef3adea60827,
        0x7bc4f7d3aaffdc1c,
        0x147d4e5953db2540
    ]
    MASK = 0xa79a63f585d37bf0 # 1010011110011010011000111111010110000101110100110111101111110000

    n = challenge & 7 #[0,7]
    # Example
    # a5       98       91       4c       81       44       00       4d
    # 10100101 10011000 10010001 01001100 10000001 01000100 00000000 01001101
    # 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000111
    # 														      => 5


    # Rotate right by 0-7 bytes
    v = rol8n(challenge, n)

    # Example
    # a5       98       91       4c       81       44       00       4d       (n=5, rotate by 4 bytes)
    # 10100101 10011000 10010001 01001100 10000001 01000100 00000000 01001101
    # =>
    # 4c       81       44       00       4d       a5       98       91
    # 01001100 10000001 01000100 00000000 01001101 10100101 10011000 10010001


    # last bit      #01111000, last bit. N: [3-6]: 1, else: 0.
    if (v & 1) == ((0x96 >> n) & 1):
        k = AUTH_EVEN_TBL[n]
    else:
        v = v ^ rol8(v) # XOR rolled, why??
        k = AUTH_ODD_TBL[n]

    return v ^ (rol8(v) & MASK) ^ k


## to pass the auth handshake sequence with davinci. This doesn't actually impact if the device functions or not lol
## maybe in the future this controls sleeping
class AuthenticationModule(SpeedEditorModule):
    # registration info
    feature_id = 0x06

    class State:
        Unauthenticated: int = const(0)  # aka SendChallenge, send challenge at this point if get_feature_report is called
        ReceiveChallenge: int = const(1)
        SendAnswer: int = const(2)
        ReceiveAnswer: int = const(3)
        Authenticated: int = const(4)

    REAUTH_DURATION: int = 600 # after this many seconds the keyboard requires a re-auth to continue working, probably for auto-sleep?
    # TODO: impl reauth timer


    def __init__(self, interface):
        super().__init__(interface)
        # i hate how python handles class attributes god
        self.kbd_solv_challenge: int = 0
        self.kbd_solv_answer: int = 0

        self.pc_solv_challenge: int = 0
        self.pc_solv_answer: int = 0

        self.stage: int = 0

        self.reset()

    # should be triggered by timeout
    def reset(self):
        self.stage = self.State.Unauthenticated

        self.pc_solv_challenge = 0x0
        self.pc_solv_answer = 0x0
        self.kbd_solv_challenge = 0x0
        self.kbd_solv_answer = 0x0

        self.generate_challenge()

    def generate_challenge(self):
        print("Generating challenge...")
        self.pc_solv_challenge = int.from_bytes(urandom(8), "little")
        self.pc_solv_answer = pc_solve_challenge(self.pc_solv_challenge)
        print("Challenge generated.")

    ## when PC sends a set feature report
    def set_feature_report(self, report_data:bytes) -> bool:
        # sanity check
        if report_data[0] != self.feature_id:
            print("MISMATCH BETWEEN SET AUTH REPORT SIGNATURE AND ID")
            return False

        report_stage = report_data[1]

        if report_stage == self.State.Unauthenticated:
            # reset self.State machine, doesn't matter what self.State it originally is
            self.reset()
            return True

        elif report_stage == self.State.ReceiveChallenge:

            if self.stage != self.State.Unauthenticated:
                # wrong auth order, reset
                self.reset()
                return False

            self.stage = self.State.ReceiveChallenge
            self.kbd_solv_challenge = int.from_bytes(report_data[2:], "little")
            print("Solving challenge...")
            self.kbd_solv_answer = kbd_solve_challenge(self.kbd_solv_challenge)
            print("Challenge solved!")
            self.stage = self.State.SendAnswer

            return True

        elif report_stage == self.State.SendAnswer:
            print("Received set report of stage SendAnswer, this is invalid!")
            return False

        elif report_stage == self.State.ReceiveAnswer:

            if self.stage != self.State.SendAnswer:
                print(f"Incorrect auth order! 04 expects 3(sendAnswer), but current internal self.State is {self.stage}")
                self.reset()
                return False

            self.stage = self.State.ReceiveAnswer

            pc_actual_answer = int.from_bytes(report_data[2:], "little")

            if pc_actual_answer == self.pc_solv_answer:
                # correct!
                self.stage = self.State.Authenticated
                return True
            else:
                # incorrect :o
                self.reset()
                return False

        elif report_stage == self.State.Authenticated:
            print("Received set report of stage Authenticated, this is invalid!")
            return False

        else:
            # should be impossible
            print(f"Invalid report stage {report_stage}!")
            return False


    ## when PC sends a get feature report request
    def get_feature_report(self):
        if self.stage == self.State.Unauthenticated: # aka send challenge
            return bytearray([self.stage]) + self.pc_solv_challenge.to_bytes(8, "little")

        elif self.stage == self.State.ReceiveChallenge:
            print("Received get feature report while in ReceiveChallenge stage. This should be impossible!")
            return False

        elif self.stage == self.State.SendAnswer:
            return bytearray([self.stage]) + self.kbd_solv_answer.to_bytes(8, "little")

        elif self.stage == self.State.ReceiveAnswer:
            print("Received get feature report while in ReceiveAnswer stage. This should be impossible!")
            return False

        elif self.stage == self.State.Authenticated:
            return bytearray([self.stage]) + self.REAUTH_DURATION.to_bytes(2, "little")

        else:
            # should be impossible
            print(f"Invalid internal stage {self.stage}!")
            return False
# Adapted from Sylvain Munaut's bmd.py (Apache 2.0 Licensed), with additional information from CommandPost (MIT/All rights reserved?)
# keys (as in dictionary keys) for speed editor related bit values.
from collections import OrderedDict

from micropython import const


class SpeedEditorKeyConstant:
	# For double press/hold emulation. All speed editor key states are directly piped to the PC, double-press/hold is
	# processed through software by Davinci resolve.
	# This project provides firmware emulation of these signals, allowing remapping of dual-purpose key actions.

	# all time variables are in milliseconds.

	PRESS_HOLD_DURATION = 80

	# adapted from CommandPost (MIT Licensed)
	# how many seconds a key must be pressed down to be considered a long press by Davinci.
	LONG_PRESS_DURATION = 400

	# double press emulation
	# The system will emulate holding the key for X seconds, release for Y seconds, then hold again for X seconds (then release).
	DOUBLE_PRESS_RELEASE_DURATION = 100

class SpeedEditorJogConstant:
	# The max/min values the knob will report.
	# in absolute mode, reported values will be clamped within these
	# in relative mode, the internal angle variable will be wrapped inside this range upon mode change.
	MIN_VAL = -4096
	MAX_VAL = 4096

	# For DEADZERO. The range in which ABSOLUTE_DEADZERO reports 0.
	DEADZERO_MIN = -300
	DEADZERO_MAX = 300

	FINE_MULTIPLIER = 12 # quarter turn = one frame

# Key Presses are reported in Input Report ID 4 as an array of 6 LE16 keycodes
# that are currently being held down. 0x0000 is no key. No auto-repeat, no hw
# detection of the 'fast double press'. Every time the set of key being held
# down changes, a new report is sent.
class SpeedEditorKey:

	NONE			= 0x00	# /

	SMART_INSRT		= 0x01	# SMART INSRT [CLIP]
	APPND			= 0x02	# APPND [CLIP]
	RIPL_OWR		= 0x03	# RIPL O/WR
	CLOSE_UP		= 0x04	# CLOSE UP [YPOS]
	PLACE_ON_TOP	= 0x05	# PLACE ON TOP
	SRC_OWR			= 0x06	# SRC O/WR

	IN				= 0x07	# IN [CLR]
	OUT				= 0x08	# OUT [CLR]
	TRIM_IN			= 0x09	# TRIM IN
	TRIM_OUT		= 0x0a	# TRIM OUT
	ROLL			= 0x0b	# ROLL [SLIDE]
	SLIP_SRC		= 0x0c	# SLIP SRC
	SLIP_DEST		= 0x0d	# SLIP DEST
	TRANS_DUR		= 0x0e	# TRANS DUR [SET]
	CUT				= 0x0f	# CUT
	DIS				= 0x10	# DIS
	SMTH_CUT		= 0x11	# SMTH CUT

	SOURCE			= 0x1a	# SOURCE
	TIMELINE		= 0x1b	# TIMELINE

	SHTL			= 0x1c	# SHTL
	JOG				= 0x1d	# JOG
	SCRL			= 0x1e	# SCRL

	ESC				= 0x31	# ESC [UNDO]
	SYNC_BIN		= 0x1f	# SYNC BIN
	AUDIO_LEVEL		= 0x2c	# AUDIO LEVEL [MARK]
	FULL_VIEW		= 0x2d	# FULL VIEW [RVW]
	TRANS			= 0x22	# TRANS [TITLE]
	SPLIT			= 0x2f	# SPLIT [MOVE]
	SNAP			= 0x2e	# SNAP [=]
	RIPL_DEL		= 0x2b	# RIPL DEL

	CAM1			= 0x33	# CAM1
	CAM2			= 0x34	# CAM2
	CAM3			= 0x35	# CAM3
	CAM4			= 0x36	# CAM4
	CAM5			= 0x37	# CAM5
	CAM6			= 0x38	# CAM6
	CAM7			= 0x39	# CAM7
	CAM8			= 0x3a	# CAM8
	CAM9			= 0x3b	# CAM9
	LIVE_OWR		= 0x30	# LIVE O/WR [RND]
	VIDEO_ONLY		= 0x25	# VIDEO ONLY
	AUDIO_ONLY		= 0x26	# AUDIO ONLY
	STOP_PLAY		= 0x3c	# STOP/PLAY

	keycode_dict = OrderedDict([
		("SMART INSRT / CLIP", SMART_INSRT),
		("APPND / CLIP", APPND),
		("RIPL OWR", RIPL_OWR),
		("CLOSE UP / YPOS", CLOSE_UP),
		("PLACE ON TOP", PLACE_ON_TOP),
		("SRC OWR", SRC_OWR),

		("IN / CLR", IN),
		("OUT / CLR", OUT),
		("TRIM IN", TRIM_IN),
		("TRIM OUT", TRIM_OUT),
		("ROLL / SLIDE", ROLL),
		("SLIP SRC", SLIP_SRC),
		("SLIP DEST", SLIP_DEST),
		("TRANS DUR / SET", TRANS_DUR),
		("CUT", CUT),
		("DIS", DIS),
		("SMTH CUT", SMTH_CUT),

		("ESC / UNDO", ESC),
		("SYNC BIN", SYNC_BIN),
		("AUDIO LEVEL / MARK", AUDIO_LEVEL),
		("FULL_VIEW / RVW", FULL_VIEW),
		("TRANS / TITLE", TRANS),
		("SPLIT / MOVE", SPLIT),
		("SNAP / RESIZE", SNAP),
		("RIPL DEL", RIPL_DEL),

		("CAM 1", CAM1),
		("CAM 2", CAM2),
		("CAM 3", CAM3),
		("CAM 4", CAM4),
		("CAM 5", CAM5),
		("CAM 6", CAM6),
		("CAM 7", CAM7),
		("CAM 8", CAM8),
		("CAM 9", CAM9),

		("LIVE OWR / RND", LIVE_OWR),
		("VIDEO ONLY", VIDEO_ONLY),
		("AUDIO ONLY", AUDIO_ONLY),

		("STOP/PLAY", STOP_PLAY),

		("SOURCE", SOURCE),
		("TIMELINE", TIMELINE),

		("SHTL", SHTL),
		("JOG", JOG),
		("SCRL", SCRL)
	])

	keyname_dict = dict((v, k) for k, v in keycode_dict.items())


# Setting the leds is done with SET_REPORT on Output Report ID 2
# which takes a single LE32 bitfield of the LEDs to enable
class SpeedEditorLed:

	CLOSE_UP	= (1 <<  0)
	CUT			= (1 <<  1)
	DIS			= (1 <<  2)
	SMTH_CUT	= (1 <<  3)
	TRANS		= (1 <<  4)
	SNAP		= (1 <<  5)
	CAM7		= (1 <<  6)
	CAM8		= (1 <<  7)
	CAM9		= (1 <<  8)
	LIVE_OWR	= (1 <<  9)
	CAM4		= (1 << 10)
	CAM5		= (1 << 11)
	CAM6		= (1 << 12)
	VIDEO_ONLY	= (1 << 13)
	CAM1		= (1 << 14)
	CAM2		= (1 << 15)
	CAM3		= (1 << 16)
	AUDIO_ONLY	= (1 << 17)
	
	name_dict = OrderedDict([
		(CLOSE_UP	, "CLOSE UP / YPOS"	),
		(CUT		, "CUT"				),
		(DIS		, "DIS"				),
		(SMTH_CUT	, "SMTH_CUT"		),
		(TRANS	 	, "TRANS / TITLE"	),
		(SNAP		, "SNAP / RESIZE"	),
		(CAM7		, "CAM 7"			),
		(CAM8		, "CAM 8"			),
		(CAM9		, "CAM 9"			),
		(LIVE_OWR	, "LIVE OWR / RND"	),
		(CAM4		, "CAM 4"			),
		(CAM5		, "CAM 5"			),
		(CAM6		, "CAM 6"			),
		(VIDEO_ONLY , "VIDEO ONLY"		),
		(CAM1		, "CAM 1"			),
		(CAM2		, "CAM 2"			),
		(CAM3		, "CAM 3"			),
		(AUDIO_ONLY , "AUDIO ONLY"		)
	])


# The LEDs for the Jog mode button are on a different system ...
# Setting those leds is done with SET_REPORT on Output Report ID 4
# which takes a single 8 bits bitfield of the LEDs to enable
class SpeedEditorJogLed:

	JOG			= (1 << 0)
	SHTL		= (1 << 1)
	SCRL		= (1 << 2)



# SHTL is 3,
# JOG is 2,
# SCRL is 2,
# Positive = clockwise
class SpeedEditorJogMode:

	RELATIVE			= 0		# Relative deltas
	ABSOLUTE_CONTINUOUS	= 1		# Send an "absolute" position (based on the position when mode was set) -4096 <- 0 -> 4096 range ~ half a turn
	RELATIVE_FINE			= 2		# Relative (Fine Control), basically 0 with higher sensitivity. Seems to have no multipliers?
	ABSOLUTE_DEADZERO	= 3		# Same as mode 1 but with a small dead band around zero that maps to 0
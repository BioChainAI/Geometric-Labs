"""CR-0001: Lamport one-time passwords, geometric adaptation research."""
from .lamport import LamportClient, LamportServer, build_chain, chain_value, new_seed, sha256
from .tile_frame import FRAME_PROFILE, FrameVerifier, decode_frame, encode_frame

__version__ = "0.1.0"
RESEARCH_ID = "CR-0001"

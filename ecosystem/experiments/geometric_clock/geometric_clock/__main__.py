"""Finite logical clock service: exact JSON snapshots, with optional JSONL ticks."""
import argparse
import json
from fractions import Fraction
from typing import Dict, Sequence

from . import ClockState, EinsteinTile, IntrinsicClock, ParityHandshakeTest, SEMANTIC_PROFILE_ID


def rational(value: Fraction) -> Dict[str, str]:
    return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}


def snapshot(state: ClockState, tile: EinsteinTile) -> Dict[str, object]:
    return {'schema': 'geometric-clock.state.v1', 'semantic_profile_id': SEMANTIC_PROFILE_ID,
            'pulse_count': str(state.pulse_count), 'node': state.node, 'spinor_step': state.spinor_step,
            'channel_id': state.channel.channel_id, 'braid': state.channel.braid,
            'elapsed_seconds': rational(state.elapsed_seconds),
            'accumulated_cycles': rational(state.accumulated_cycles),
            'atomic_residual': rational(state.atomic_residual), 'tile_hex': f'{tile.pack():016x}',
            'epoch_id': state.epoch_id, 'frame_id': state.frame_id,
            'time_uncertainty': rational(state.time_uncertainty)}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pulses', type=int, default=30)
    parser.add_argument('--stream', action='store_true', help='emit one JSON record per logical pulse')
    parser.add_argument('--verify-sync', action='store_true', help='run the two-clock local handshake simulation')
    args = parser.parse_args(argv)
    if args.pulses < 0:
        parser.error('pulses must be nonnegative')
    if args.verify_sync and args.stream:
        parser.error('choose either stream or verify-sync')
    if args.verify_sync:
        try:
            report = ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock(), pulses=args.pulses)
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps({'schema': 'geometric-clock.handshake.v1', 'success': report.success,
                          'start_pulse': str(report.start_pulse), 'end_pulse': str(report.end_pulse),
                          'exchanges': len(report.exchanges), 'phase_drift': rational(report.phase_drift),
                          'holonomy1': [str(q) for q in report.holonomy1.as_tuple()],
                          'holonomy2': [str(q) for q in report.holonomy2.as_tuple()]}))
    else:
        clock = IntrinsicClock()
        if args.stream:
            for _ in range(args.pulses):
                print(json.dumps(snapshot(*clock.step_pulse())), flush=True)
        else:
            print(json.dumps(snapshot(*clock.advance(args.pulses))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

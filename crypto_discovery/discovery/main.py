import argparse
import json
import os

from .adapters import CompositeDiscovery, DexScreenerAdapter, GeckoTerminalAdapter
from .firebase_sink import FirebaseDiscoverySink
from .service import DiscoveryService


def main():
    parser = argparse.ArgumentParser(description="BrAInChain new-token discovery")
    parser.add_argument(
        "--pages",
        type=int,
        default=int(os.getenv("DISCOVERY_PAGES", "1")),
        help="GeckoTerminal new-pool pages to scan (public API: 20 pools/page).",
    )
    parser.add_argument("--firebase", action="store_true")
    args = parser.parse_args()

    service = DiscoveryService(
        CompositeDiscovery(
            [
                GeckoTerminalAdapter(pages=max(1, args.pages)),
                DexScreenerAdapter(),
            ]
        )
    )
    result = service.run()
    print(json.dumps({"pools": len(result.pools), "errors": result.errors}, indent=2))

    if args.firebase:
        payload = FirebaseDiscoverySink().write(result.pools, result.errors)
        print(json.dumps(payload, indent=2))

    if not result.pools and result.errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

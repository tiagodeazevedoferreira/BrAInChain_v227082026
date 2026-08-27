import argparse
import json
import os

from .engine import IntelligenceEngine
from .firebase_sink import FirebaseMarketSink
from .providers import DexScreenerMarketProvider, GeckoTerminalTradeProvider


def main():
    parser = argparse.ArgumentParser(description="BrAInChain Market & On-chain Intelligence")
    parser.add_argument("--firebase", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=int(os.getenv("MARKET_MAX_TOKENS", "25")))
    args = parser.parse_args()

    import firebase_admin
    from firebase_admin import credentials, db

    cred_file = os.getenv("FIREBASE_SERVICE_ACCOUNT_FILE")
    if not cred_file:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_FILE is required")
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(
            credentials.Certificate(cred_file),
            {"databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://brainchainv227082026-default-rtdb.firebaseio.com")},
        )

    tokens = db.reference("/discovery/tokens", app=app).get() or {}
    engine = IntelligenceEngine(DexScreenerMarketProvider(), GeckoTerminalTradeProvider())
    analyses = []
    errors = []
    for item in list(tokens.values())[: max(0, args.max_tokens)]:
        network = item.get("network")
        token = item.get("base_token_address")
        pool = item.get("pool_address")
        if not network or not token or not pool:
            continue
        try:
            analyses.append(engine.analyze(network, token, pool))
        except Exception as exc:
            errors.append({"token": token, "error": str(exc)})

    payload = {"analyzed": len(analyses), "errors": errors}
    print(json.dumps(payload, indent=2))
    if args.firebase:
        status = FirebaseMarketSink().write(analyses, errors)
        print(json.dumps(status, indent=2))

    if not analyses and errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

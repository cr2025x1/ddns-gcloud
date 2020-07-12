import argparse

action_parser = argparse.ArgumentParser(add_help=False)
subparsers = action_parser.add_subparsers(title='actions', dest='action')
subparsers.required = True

add_parser = subparsers.add_parser("add")
add_parser.add_argument("--zone", help="Zone name from Google DNS.")
add_parser.add_argument("--acme_challenge_token", help="ACME challenge token for Let's Encrypt certificate operation.")

cleanup_parser = subparsers.add_parser("cleanup")
cleanup_parser.add_argument("--zone", help="Zone name from Google DNS.")
cleanup_parser.add_argument("--domain", help="Domain name you want to renew.")

if __name__ == "__main__":
    args = action_parser.parse_args()

    if args.action == 'add':
        print(f"Zone: {args.zone}")
        print(f"ACME challenge token: {args.acme_challenge_token}")
    elif args.action == 'cleanup':
        print(f"Zone: {args.zone}")
        print(f"Domain: {args.domain}")

    print("Hello, world!")
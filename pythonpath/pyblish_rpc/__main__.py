import server

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=6000,
                        help="Port to use")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Higher value means slower")
    parser.add_argument("--debug", action="store_true", default=False)

    args = parser.parse_args()

    if args.debug:
        print "Starting debug server.."
        server.start_debug_server(**args.__dict__)
    else:
        print "Starting production server.."
        server.start_production_server(port=args.port)

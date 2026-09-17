def main(argv=None) -> int:
    """Entry point for python -m pyrepofile."""
    import sys
    from pyrepofile.cli import main as cli_main
    args = sys.argv[1:] if argv is None else argv
    return cli_main(args)


if __name__ == "__main__":
    main()

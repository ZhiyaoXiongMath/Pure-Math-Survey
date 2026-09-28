#!/usr/bin/env python3
"""Native Pure Math Survey 2.0.0 entry point; also runs under Python -I."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from survey_core.cli import main
if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/bash

sed -i "s/%define inochi_session_ver .*/%define inochi_session_ver $1/" inochi-session-nightly.spec
sed -i "s/%define inochi_session_dist .*/%define inochi_session_dist $2/" inochi-session-nightly.spec
sed -i "s/%define inochi_session_short .*/%define inochi_session_short $3/" inochi-session-nightly.spec

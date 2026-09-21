#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/MW_CENTRAL/TRIANGULUM/hermes-spl-fork')
# Test that the gateway module can import the activity functions
try:
    from gateway.platforms import api_server
    print("api_server module imported OK")
    print("Has _cron_activity_list:", hasattr(api_server, '_cron_activity_list'))
    print("Has _cron_activity_detail:", hasattr(api_server, '_cron_activity_detail'))
    print("Has _handle_cron_activity:", hasattr(api_server.APIServerAdapter, '_handle_cron_activity'))
    print("Has _handle_cron_activity_detail:", hasattr(api_server.APIServerAdapter, '_handle_cron_activity_detail'))
except Exception as e:
    print(f"Import error: {e}")

set FNCS_FATAL=yes
set FNCS_LOG_STDOUT=yes
set FNCS_LOG_LEVEL=INFO
set FNCS_TRACE=yes
set SCHEDULE_PORT=5550
set WEATHER_CONFIG=weather_Config.json
set with_market=1
IF "%1"=="base" set with_market=0
start /b cmd /c python -c "import tesp_support.schedule_server as schedule;schedule.schedule_server(5550)" ^> .\schedule.log 2^>^&1
rem wait schedule server to populate
sleep 50
start /b cmd /c fncs_broker 6 ^>.\broker.log 2^>^&1
set FNCS_CONFIG_FILE=weather_Substation_1.zpl
cd weather_Substation_1
start /b cmd /c python -c "import tesp_support.api as tesp;tesp.startWeatherAgent('weather.dat')" ^> .\weather_Substation_1_weather.log 2^>^&1
cd ..
cd Substation_1
start /b cmd /c gridlabd -D USE_FNCS -D METRICS_FILE="Substation_1_metrics_" Substation_1.glm ^> .\Substation_1_gridlabd.log 2^>^&1
set FNCS_CONFIG_FILE=Substation_1.yaml
cd ..
cd DSO_1
start /b cmd /c python -c "import tesp_support.substation_dsot_v1 as tesp;tesp.substation_loop('Substation_1_agent_dict.json','Substation_1',%with_market%)" ^> .\DSO_1_substation.log 2^>^&1
cd ..
set FNCS_CONFIG_FILE=tso.yaml
start /b cmd /c python -c "import tesp_support.fncsTSO as tesp;tesp.tso_loop('./system_case_config_mod')" ^> .\tso.log 2^>^&1
set FNCS_CONFIG_FILE=load_player.yaml
start /b cmd /c python -c "import tesp_support.load_player as tesp;tesp.load_player_loop('./system_case_config_mod', 'keyLoad')" ^> .\load_player.log 2^>^&1
set FNCS_CONFIG_FILE=wind_player.yaml
start /b cmd /c python -c "import tesp_support.load_player as tesp;tesp.load_player_loop('./system_case_config_mod', 'keyGen')" ^> .\wind_player.log 2^>^&1

### mqtt-receiver-python industial service


{
  "name": "MQTT Python"
}


                          MQTT BROKER
                              │
                              ▼
                       callback MQTT
                              │
                    crea un mensaje
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
            LOG_QUEUE                  DB_QUEUE
                 │                         │
                 ▼                         ▼
         log_writer thread           db_writer thread
                 │                         │
                 ▼                         ▼
      data/YYYY/MM.log           PostgreSQL Pool
                                           │
                                           ▼
                                  mqtt_record_lines
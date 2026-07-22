module.exports = {
  apps: [
    {
      name: "randevumonline-voice-large-test",
      cwd: "/home/randevumonline_chatbot",
      script: "/home/randevumonline_chatbot/.venv/bin/python",
      args: "-m uvicorn app.voice.service:app --host 127.0.0.1 --port 9020",
      interpreter: "none",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false,
      min_uptime: "30s",
      max_restarts: 20,
      restart_delay: 5000,
      kill_timeout: 15000,
      max_memory_restart: "4G",
      time: true,
      env: {
        PYTHONUNBUFFERED: "1",
        PYTHONPATH: "/home/randevumonline_chatbot",
        OMP_NUM_THREADS: "4",
        VOICE_STT_FAST_MODEL: "small",
        VOICE_STT_ACCURATE_MODEL: "small",
      },
    },
  ],
};

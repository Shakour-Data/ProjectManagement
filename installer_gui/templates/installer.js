new QWebChannel(qt.webChannelTransport, function(channel) {
    window.backend = channel.objects.backend;

    const statusDiv = document.getElementById('status');
    const startBtn = document.getElementById('startBtn');

    startBtn.addEventListener('click', () => {
        startBtn.disabled = true;
        statusDiv.textContent = 'Starting installation...';
        backend.startInstallation();
    });

    backend.updateStatus.connect(function(message) {
        statusDiv.textContent = message;
    });
});

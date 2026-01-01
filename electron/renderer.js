const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    openExternal: (url) => ipcRenderer.invoke('open-external', url),
    getVersion: () => ipcRenderer.invoke('get-version'),
    minimize: () => ipcRenderer.invoke('minimize'),
    maximize: () => ipcRenderer.invoke('maximize'),
    close: () => ipcRenderer.invoke('close')
});

// Add Fox AI specific functionality
contextBridge.exposeInMainWorld('foxAPI', {
    // Add any Fox-specific APIs here
    log: (message) => console.log('Fox AI:', message),
    notify: (title, body) => {
        new Notification(title, { body });
    }
});

// Enhance the web interface with desktop features
window.addEventListener('DOMContentLoaded', () => {
    // Add desktop-specific styling
    document.body.classList.add('electron-app');
    
    // Add window controls if needed
    const titleBar = document.querySelector('.title-bar');
    if (titleBar) {
        titleBar.style.display = 'none'; // Hide web title bar in desktop app
    }
    
    // Enhance notifications
    if ('Notification' in window) {
        Notification.requestPermission();
    }
});

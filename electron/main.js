const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let webServer;

function startWebServer() {
    return new Promise((resolve, reject) => {
        console.log('🚀 Starting Fox AI web server...');
        
        // Start the Python web server
        webServer = spawn('python', ['start_web.py'], {
            cwd: path.join(__dirname, '..'),
            stdio: 'pipe'
        });
        
        webServer.stdout.on('data', (data) => {
            console.log(`Server: ${data}`);
            if (data.toString().includes('Uvicorn running')) {
                resolve();
            }
        });
        
        webServer.stderr.on('data', (data) => {
            console.error(`Server Error: ${data}`);
        });
        
        webServer.on('close', (code) => {
            console.log(`Server process exited with code ${code}`);
        });
        
        // Timeout after 10 seconds
        setTimeout(() => {
            resolve(); // Continue anyway
        }, 10000);
    });
}

async function createWindow() {
    // Start web server first
    await startWebServer();
    
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'renderer.js')
        },
        icon: path.join(__dirname, 'icon.png'),
        title: 'Fox AI Assistant',
        titleBarStyle: 'default',
        show: false
    });

    // Load the web interface
    mainWindow.loadURL('http://localhost:8080');

    // Show window when ready
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Handle window closed
    mainWindow.on('closed', () => {
        mainWindow = null;
        // Kill web server when window closes
        if (webServer) {
            webServer.kill();
        }
    });

    // Open external links in browser
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    // Create menu
    createMenu();
}

function createMenu() {
    const template = [
        {
            label: 'Fox AI',
            submenu: [
                {
                    label: 'درباره Fox AI',
                    click: () => {
                        const aboutWindow = new BrowserWindow({
                            width: 400,
                            height: 300,
                            parent: mainWindow,
                            modal: true,
                            show: false,
                            resizable: false
                        });
                        aboutWindow.loadFile(path.join(__dirname, 'about.html'));
                        aboutWindow.once('ready-to-show', () => {
                            aboutWindow.show();
                        });
                    }
                },
                { type: 'separator' },
                {
                    label: 'خروج',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'ویرایش',
            submenu: [
                { label: 'برش', accelerator: 'CmdOrCtrl+X', role: 'cut' },
                { label: 'کپی', accelerator: 'CmdOrCtrl+C', role: 'copy' },
                { label: 'چسباندن', accelerator: 'CmdOrCtrl+V', role: 'paste' },
                { type: 'separator' },
                { label: 'انتخاب همه', accelerator: 'CmdOrCtrl+A', role: 'selectall' }
            ]
        },
        {
            label: 'نمایش',
            submenu: [
                { label: 'بازخوانی', accelerator: 'CmdOrCtrl+R', role: 'reload' },
                { label: 'بازخوانی اجباری', accelerator: 'CmdOrCtrl+Shift+R', role: 'forceReload' },
                { label: 'ابزار توسعه‌دهنده', accelerator: 'F12', role: 'toggleDevTools' },
                { type: 'separator' },
                { label: 'تمام صفحه', accelerator: 'F11', role: 'togglefullscreen' }
            ]
        },
        {
            label: 'پنجره',
            submenu: [
                { label: 'کمینه کردن', accelerator: 'CmdOrCtrl+M', role: 'minimize' },
                { label: 'بستن', accelerator: 'CmdOrCtrl+W', role: 'close' }
            ]
        },
        {
            label: 'راهنما',
            submenu: [
                {
                    label: 'راهنمای Fox AI',
                    click: () => {
                        shell.openExternal('https://github.com/theistthirteenmm/Fox_Ai');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    // Kill web server
    if (webServer) {
        webServer.kill();
    }
    
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

app.on('before-quit', () => {
    // Kill web server before quitting
    if (webServer) {
        webServer.kill();
    }
});

// Security: Prevent new window creation
app.on('web-contents-created', (event, contents) => {
    contents.on('new-window', (event, navigationUrl) => {
        event.preventDefault();
        shell.openExternal(navigationUrl);
    });
});

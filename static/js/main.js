if ('serviceWorker' in navigator && 'SyncManager' in window) {
    navigator.serviceWorker.register("/service-worker.js").then(registration => {
        console.log('Service Worker registered with scope:', registration.scope);
        // console.log(`A service worker is active: ${registration.active.state}`);
        // registration.sync.register('sync-tasks').then(() => {
        //     console.log('Sync registered');
        // }).catch(err => {
        //     console.error('Sync registration failed:', err);
        // });
    }).catch(error => {
        console.error('Service Worker registration failed:', error);
    });
} else {
    console.log('Service Worker or Background Sync is not supported in this browser');
}

// if ('Notification' in window && 'serviceWorker' in navigator) {
//     Notification.requestPermission().then(permission => {
//         // $('#allow-push-notification-bar').hide();
//         // buat tombol untuk di klik dulu untuk konfirmasi izin notfikasi biar gak error di Edge dan Mozilla!
//         if (permission === 'granted') {
//             console.log('Notification permission granted.');
//         } else {
//             console.log('Notification permission denied.');
//         }
//     });
// }

  
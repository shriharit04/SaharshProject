const wbm = require('wbm');

wbm.start().then(async () => {
    const phones = ['919789114693'];
    const message = 'Good Morning.';
    await wbm.send(phones, message);
    await wbm.end();
}).catch(err => console.log(err));

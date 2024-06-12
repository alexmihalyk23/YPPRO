const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Путь к файлу index.html в папке templates
    const filePath = `file://${path.join(__dirname, '/templates/index.html')}`;
    await page.goto(filePath);

    const fileInput = await page.$('#zipFile');
    const sendButton = await page.$('#sendButton');

    // Проверяем, что кнопка отправки сначала отключена
    const isDisabled = await page.evaluate(button => button.disabled, sendButton);
    console.assert(isDisabled, 'Send button should be disabled initially');

    // Замените на путь к вашему zip файлу
    await fileInput.uploadFile(path.join(__dirname, 'test.zip'));

    // Проверяем, что кнопка отправки включена после загрузки файла
    const isEnabled = await page.evaluate(button => !button.disabled, sendButton);
    console.assert(isEnabled, 'Send button should be enabled after file upload');

    await browser.close();
})();

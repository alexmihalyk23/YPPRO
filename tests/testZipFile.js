const puppeteer = require('puppeteer');
const assert = require('assert');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('file://' + path.resolve(__dirname, 'index.html'));

    const fileInput = await page.$('#zipFile');
    const sendButton = await page.$('#sendButton');
    const selectButton = await page.$('#selectButton');

    // Создание пустого файла для теста
    const emptyZipPath = path.resolve(__dirname, 'empty.zip');
    const fs = require('fs');
    fs.writeFileSync(emptyZipPath, '');

    // Загрузка пустого файла
    await fileInput.uploadFile(emptyZipPath);

    // Проверка состояния кнопок
    const sendButtonDisabled = await page.evaluate(button => button.disabled, sendButton);
    const selectButtonText = await page.evaluate(button => button.innerText, selectButton);

    assert.strictEqual(sendButtonDisabled, false, 'Send button should be enabled');
    assert.strictEqual(selectButtonText, 'File is loaded', 'Select button text should be "File is loaded"');

    await browser.close();
})();

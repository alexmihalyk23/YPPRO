const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
    const templatesDir = path.resolve(__dirname, '../templates');
    
    // Проверка наличия папки
    if (!fs.existsSync(templatesDir)) {
        console.error(`Directory not found: ${templatesDir}`);
        process.exit(1);
    }

    // Вывод содержимого папки
    console.log(`Contents of ${templatesDir}:`);
    const files = fs.readdirSync(templatesDir);
    files.forEach(file => {
        console.log(file);
    });

    // Проверка наличия файла main.html
    const filePath = path.join(templatesDir, 'main.html');
    if (!fs.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        process.exit(1);
    }

    // Вывод содержимого файла
    console.log(`\nFile found: ${filePath}`);
    const fileContent = fs.readFileSync(filePath, 'utf8');
    console.log(`File content:\n${fileContent}\n`);

    // Запуск браузера Puppeteer и выполнение теста
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`file://${filePath}`);

    const fileInput = await page.$('#zipFile');
    const sendButton = await page.$('#sendButton');

    // Проверка, что кнопка отправки сначала отключена
    const isDisabled = await page.evaluate(button => button.disabled, sendButton);
    console.assert(isDisabled, 'Send button should be disabled initially');

    // Замените на путь к вашему zip файлу
    await fileInput.uploadFile(path.join(__dirname, 'test.zip'));

    // Проверка, что кнопка отправки включена после загрузки файла
    const isEnabled = await page.evaluate(button => !button.disabled, sendButton);
    console.assert(isEnabled, 'Send button should be enabled after file upload');

    await browser.close();
})();

// @ts-ignore: Playwright types may not be installed locally
import { test, expect } from '@playwright/test';

test('Mahasiswa mengajukan pendaftaran beasiswa', async ({ page }: { page: any }) => {
  await page.goto('http://127.0.0.1:8000/login');

  const username = page.locator('input[name="username"]');
  const password = page.locator('input[name="password"]');
  const loginBtn = page.locator('button:has-text("Login")');

  await username.fill('intan');
  await password.fill('password123');
  await loginBtn.click();

  await page.locator('text=Apply Scholarship').click();

  await page.locator('input[name="nama_lengkap"]').fill('Intan Sarinah');
  await page.locator('input[name="nim"]').fill('2208079654');
  await page.locator('input[name="ipk"]').fill('3.5');
  await page.locator('input[name="jumlah_juz"]').fill('15');

  await page.locator('button:has-text("Kirim")').click();

  await expect(page.locator('text=/berhasil/i')).toBeVisible();
});

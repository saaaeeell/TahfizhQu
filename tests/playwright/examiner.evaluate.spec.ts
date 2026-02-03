// @ts-ignore: Playwright types may not be installed locally
import { test, expect } from '@playwright/test';

test('Penguji menginput nilai tahfizh', async ({ page }: { page: any }) => {
  await page.goto('http://127.0.0.1:8000/login');

  const username = page.locator('input[name="username"]');
  const password = page.locator('input[name="password"]');
  const loginBtn = page.locator('button:has-text("Login")');

  await username.fill('Indy');
  await password.fill('password123');
  await loginBtn.click();

  await page.locator('text=Beri Penilaian').click();

  await page.locator('input[name="makhorijul"]').fill('80');
  await page.locator('input[name="tajwid"]').fill('75');
  await page.locator('input[name="kelancaran"]').fill('85');

  await page.locator('button:has-text("Kirim Penilaian")').click();

  await expect(page.locator('text=/berhasil/i')).toBeVisible();
});

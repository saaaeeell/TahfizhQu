// @ts-ignore: Playwright types may not be installed locally
import { test, expect } from '@playwright/test';

test('Admin membuat kelompok tahfizh', async ({ page }: { page: any }) => {
  await page.goto('http://127.0.0.1:8000/login');

  const username = page.locator('input[name="username"]');
  const password = page.locator('input[name="password"]');
  const loginBtn = page.locator('button:has-text("Login")');

  await username.fill('Elsa12');
  await password.fill('password123');
  await loginBtn.click();

  await page.locator('text=Create Group').click();
  await page.locator('input[name="group_name"]').fill('Tahfizh A1');
  await page.locator('select[name="examiner"]').selectOption('2');

  await page.locator('button:has-text("Buat Kelompok")').click();

  await expect(page.locator('text=/berhasil/i')).toBeVisible();
});

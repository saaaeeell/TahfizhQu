// @ts-ignore: Playwright types may not be installed locally
import { test, expect } from '@playwright/test';

test('Login admin dengan data valid', async ({ page }: { page: any }) => {
  await page.goto('http://127.0.0.1:8000/login');

  const username = page.locator('input[name="username"]');
  const password = page.locator('input[name="password"]');
  const loginBtn = page.locator('button:has-text("Login")');

  await username.fill('Elsa12');
  await password.fill('password123');
  await loginBtn.click();

  await expect(page).toHaveURL(/dashboard/);
});

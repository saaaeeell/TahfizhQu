import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://localhost:8000';

const users = [
  { role: 'admin', username: 'bintang37a', password: 'bintang123', dashboard: '/admin/dashboard/' },
  { role: 'examiner', username: '22040700020', password: 'bintang123', dashboard: '/examiner/dashboard/' },
  { role: 'student', username: 'bintang25a', password: 'bintang123', dashboard: '/student/dashboard/' },
];

for (const user of users) {
  test.describe(`${user.role} login`, () => {
    test(`${user.username} can login and reach dashboard`, async ({ page }) => {
      await page.goto(baseURL + '/login/');
      await page.fill('input[name="username"]', user.username);
      await page.fill('input[name="password"]', user.password);
      await page.click('button[type="submit"]');
      await expect(page).toHaveURL(new RegExp(user.dashboard));
    });
  });
}

// Additional admin checks
test.describe('Admin dashboard checks', () => {
  test('Admin can open Total Pendaftar and see students list', async ({ page }) => {
    await page.goto(baseURL + '/login/');
    await page.fill('input[name="username"]', 'bintang37a');
    await page.fill('input[name="password"]', 'bintang123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(new RegExp('/admin/dashboard/'));

    // Click Total Pendaftar card (link to students)
    await page.click('a[href*="/admin/students/"]');
    await expect(page).toHaveURL(new RegExp('/admin/students/'));
    await expect(page.locator('h2')).toContainText('Daftar Mahasiswa');
  });
});

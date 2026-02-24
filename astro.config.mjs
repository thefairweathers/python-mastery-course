import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeRelativeMarkdownLinks from 'astro-rehype-relative-markdown-links';

export default defineConfig({
  site: 'https://thefairweathers.github.io',
  base: '/python-mastery-course',
  markdown: {
    rehypePlugins: [rehypeRelativeMarkdownLinks],
  },
  integrations: [
    starlight({
      title: 'Python Mastery',
      description: 'A 13-week course taking you from Python beginner to confident developer.',
      customCss: ['./src/styles/custom.css'],
      components: {
        Head: './src/components/Head.astro',
      },
      sidebar: [
        { label: 'Home', slug: 'index' },
        {
          label: 'Week 01 — Environment & Tooling',
          items: [
            { slug: 'week-01', label: 'Lesson' },
            { slug: 'week-01/lab-01-verify' },
            { slug: 'week-01/lab-02-repl' },
          ],
        },
        {
          label: 'Week 02 — Python Fundamentals',
          items: [
            { slug: 'week-02', label: 'Lesson' },
            { slug: 'week-02/lab-01-types' },
            { slug: 'week-02/lab-02-strings' },
            { slug: 'week-02/lab-03-numbers' },
          ],
        },
        {
          label: 'Week 03 — Control Flow & Logic',
          items: [
            { slug: 'week-03', label: 'Lesson' },
            { slug: 'week-03/lab-01-fizzbuzz' },
            { slug: 'week-03/lab-02-filter' },
          ],
        },
        {
          label: 'Week 04 — Functions & Scope',
          items: [
            { slug: 'week-04', label: 'Lesson' },
            { slug: 'week-04/lab-01-memoize' },
            { slug: 'week-04/lab-02-pipeline' },
          ],
        },
        {
          label: 'Week 05 — Data Structures',
          items: [
            { slug: 'week-05', label: 'Lesson' },
            { slug: 'week-05/lab-01-inventory' },
            { slug: 'week-05/lab-02-graph' },
          ],
        },
        {
          label: 'Week 06 — Object-Oriented Programming',
          items: [
            { slug: 'week-06', label: 'Lesson' },
            { slug: 'week-06/lab-01-events' },
            { slug: 'week-06/lab-02-shapes' },
          ],
        },
        {
          label: 'Week 07 — File I/O & Data Formats',
          items: [
            { slug: 'week-07', label: 'Lesson' },
            { slug: 'week-07/lab-01-config' },
            { slug: 'week-07/lab-02-logs' },
          ],
        },
        {
          label: 'Week 08 — Error Handling & Debugging',
          items: [
            { slug: 'week-08', label: 'Lesson' },
            { slug: 'week-08/lab-01-processor' },
            { slug: 'week-08/lab-02-exceptions' },
          ],
        },
        {
          label: 'Week 09 — Modules & Packages',
          items: [
            { slug: 'week-09', label: 'Lesson' },
            { slug: 'week-09/lab-01-notes' },
            { slug: 'week-09/lab-02-packaging' },
          ],
        },
        {
          label: 'Week 10 — Testing & Code Quality',
          items: [
            { slug: 'week-10', label: 'Lesson' },
            { slug: 'week-10/lab-01-testing' },
            { slug: 'week-10/lab-02-quality' },
          ],
        },
        {
          label: 'Week 11 — Advanced Patterns',
          items: [
            { slug: 'week-11', label: 'Lesson' },
            { slug: 'week-11/lab-01-pipeline' },
            { slug: 'week-11/lab-02-decorators' },
            { slug: 'week-11/lab-03-async' },
          ],
        },
        {
          label: 'Week 12 — APIs & Data Engineering',
          items: [
            { slug: 'week-12', label: 'Lesson' },
            { slug: 'week-12/lab-01-api' },
            { slug: 'week-12/lab-02-api' },
            { slug: 'week-12/lab-03-analysis' },
          ],
        },
        {
          label: 'Week 13 — AI & Machine Learning',
          items: [
            { slug: 'week-13', label: 'Lesson' },
            { slug: 'week-13/lab-01-agent' },
          ],
        },
      ],
    }),
  ],
});

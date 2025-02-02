import { getPermalink, getBlogPermalink, getAsset } from './utils/permalinks';

export const headerData = {
  // For Fort, we’re streamlining the navigation to reflect the new pages.
  links: [
    { text: 'Home', href: getPermalink('/') },
    { text: 'Events', href: getPermalink('/events') },
    { text: 'AI', href: getPermalink('/ai') },
    { text: 'Education', href: getPermalink('/education') },
    { text: 'Forum', href: getPermalink('/forum') },
    { text: 'Health & Wellness', href: getPermalink('/health-and-wellness') },
    { text: 'About', href: getPermalink('/about') },
    { text: 'Contact', href: getPermalink('/contact') },
    { text: 'Donate', href: getPermalink('/donate') },
  ],
  // Optional call-to-action button(s) can be added here if needed
  actions: [
    // For example, if you want a button that links to a resource or download
    // { text: 'Download', href: 'https://github.com/onwidget/astrowind', target: '_blank' }
  ],
};

export const footerData = {
  links: [
    {
      title: 'Company',
      links: [
        { text: 'About', href: getPermalink('/about') },
        { text: 'Contact', href: getPermalink('/contact') },
        { text: 'Donate', href: getPermalink('/donate') },
      ],
    },
    {
      title: 'Resources',
      links: [
        { text: 'Events', href: getPermalink('/events') },
        { text: 'AI', href: getPermalink('/ai') },
        { text: 'Education', href: getPermalink('/education') },
        { text: 'Forum', href: getPermalink('/forum') },
        { text: 'Health & Wellness', href: getPermalink('/health-and-wellness') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Terms', href: getPermalink('/terms') },
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
  ],
  socialLinks: [
    { ariaLabel: 'X', icon: 'tabler:brand-x', href: '#' },
    { ariaLabel: 'Instagram', icon: 'tabler:brand-instagram', href: '#' },
    { ariaLabel: 'Facebook', icon: 'tabler:brand-facebook', href: '#' },
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml') },
    { ariaLabel: 'Github', icon: 'tabler:brand-github', href: 'https://github.com/onwidget/astrowind' },
  ],
  // Update this footnote as desired for Fort (you might want to remove or rebrand the onWidget reference)
  footNote: `
    <img class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm" src="https://onwidget.com/favicon/favicon-32x32.png" alt="onWidget logo" loading="lazy" />
    Made by <a class="text-blue-600 underline dark:text-muted" href="https://onwidget.com/">onWidget</a> · All rights reserved.
  `,
};

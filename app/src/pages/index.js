import React from 'react';
import Layout from '../layouts/index';
import Hero from '../components/hero/Hero';
import HeroIllustration from '../components/hero/HeroIllustration';

export default function IndexPage() {
  return (
    <Layout>
      <Hero
        title="Bomb Not Bomb"
        content="We Scan and identify zip bombs which can cause harm to your device, and warn you accordingly"
        illustration={HeroIllustration}
      />
    </Layout>
  );
}

import React, { Component } from 'react';
import { setupScrollReveal } from '../assets/js/main.js';

import ResultForm from '../components/forms/ResultForm.js';

class Hero extends Component {
  componentDidMount() {
    setupScrollReveal();
  }

  render() {
    const { title, content, illustration: Illustration } = this.props;

    return (
      <section className="hero">
        <div className="container">
          <div className="hero-inner">
            <div className="hero-copy">
              <div className="container-sm">
                <h1 className="hero-title h2-mobile mt-0 is-revealing">
                  {title}
                </h1>
                <p className="hero-paragraph is-revealing">{content}</p>
              </div>
              <ResultForm className="hero-form" submit="Scan for me" />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default Hero;

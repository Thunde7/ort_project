import React, { Component } from 'react';
import classnames from 'classnames';

class NewsletterForm extends Component {
  constructor(props) {
    super(props);
    this.state = { username: '', filename: null };
  }

  onFileChange = (event) => {
    this.setState({ filename: event.target.files[0] });
  };

  render() {
    const { className, submit = 'Submit' } = this.props;
    const { username, filename } = this.state;

    return (
      <form
        className={classnames(
          'newsletter-form field field-grouped is-revealing',
          className
        )}
      >
        <div className="control control-expanded">
          <input
            className="input"
            type="file"
            name="filename"
            onChange={this.onFileChange}
          />
          <input
            className="input"
            type="text"
            name="username"
            placeholder="Your username"
          />
        </div>
        <div className="control">
          <button
            className="button button-primary button-block button-shadow"
            type="submit"
          >
            {submit}
          </button>
        </div>
      </form>
    );
  }
}

export default NewsletterForm;

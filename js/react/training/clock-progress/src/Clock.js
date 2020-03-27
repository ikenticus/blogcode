import React from 'react';
import ArticleProgress from './ArticleProgress';
import _ from 'lodash';
import './Clock.css';

class LongPage extends React.Component {
  renderBlock(c) {
    return (
      <div className={"LongBlock Block" + c} />
    );
  }

  render() {
    return (
      <div>
        {_.times(10, c =>
            this.renderBlock(c)
        )}
      </div>
    );
  }
}

function Clock() {
  return (
    <div className="Clock">
      <ArticleProgress
        strokeWidth="15"
        sqSize="100"
        sqTop="80"
        sqRight="50"/>
      <LongPage />
      <div className="page-end">END of PAGE</div>
    </div>
  );
}

export default Clock;

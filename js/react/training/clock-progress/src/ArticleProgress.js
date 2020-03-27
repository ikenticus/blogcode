import React, { Component, Fragment } from 'react';
import './ArticleProgress.scss';

function getDocHeight() {
  const pageEnd = document.getElementsByClassName('page-end')[0];
  return pageEnd.offsetTop;
}

class ArticleProgress extends Component {
  constructor(props) {
    super(props);
    this.state = {
      percentage: 0,
      degrees: 0,
      hourDeg: 0
    };

    this.handleScroll = this.handleScroll.bind(this);
  }

  handleScroll() {
    try {
      var winheight= window.innerHeight || (document.documentElement || document.body).clientHeight;
      var docheight = getDocHeight();
      var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
      var trackLength = docheight - winheight;
      var percentage = Math.floor(scrollTop/trackLength * 100);
      if(percentage > 100){
        percentage = 100;
      }
      var degrees = (percentage * 2.1);
      var hourDeg = (degrees/2);
      if(hourDeg > 20) {
        hourDeg = 20;
      }
      this.setState({percentage, degrees, hourDeg});

    } catch (e) {
      throw new Error('Error in handleScroll method of ArticleProgress.', e);
    }
  }

  componentDidMount() {
    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', this.handleScroll);
    }
  }

  componentWillUnmount() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('scroll', this.handleScroll);
    }
  }

  render() {
    // Size of the enclosing square
    const sqSize = this.props.sqSize;
    // SVG centers the stroke width on the radius, subtract out so circle fits in square
    const radius = (this.props.sqSize - this.props.strokeWidth) / 2;
    // Enclose cicle in a circumscribing square
    const viewBox = `0 0 ${sqSize} ${sqSize}`;
    // Arc length at 100% coverage is the circle circumference
    const dashArray = radius * Math.PI * 2;
    // Scale 100% coverage overlay with the actual percent
    const dashOffset = dashArray - dashArray * this.state.percentage / 100;

    const containerStyles = {
      top: `${this.props.sqTop}px`,
      right: `${this.props.sqRight}px`
    }

    const hourStyles = {
      transform: `rotate(${this.state.hourDeg}deg)`
    }

    const minuteStyles = {
      transform: `rotate(${this.state.degrees}deg)`
    }

    const progressBarStyles = {
      width: `${this.state.percentage}%`
    }

    let className = 'article-progress';

    if(this.state.percentage == 100) {
      className = 'article-progress complete'
    }
    //if(!this.props.isMobile) {
    return (
      <div className={className} style={containerStyles}>
      {(this.state.percentage > 0) &&
        <Fragment>
      <svg
          width={this.props.sqSize}
          height={this.props.sqSize}
          viewBox={viewBox}>
          <circle
            className="circle-background"
            cx={this.props.sqSize / 2}
            cy={this.props.sqSize / 2}
            r={radius}
            strokeWidth={`${this.props.strokeWidth}px`} />
          <circle
            className="circle-progress"
            cx={this.props.sqSize / 2}
            cy={this.props.sqSize / 2}
            r={radius}
            strokeWidth={`${this.props.strokeWidth}px`}
            // Start progress marker at 12 O'Clock
            transform={`rotate(-90 ${this.props.sqSize / 2} ${this.props.sqSize / 2})`}
            style={{
              strokeDasharray: dashArray,
              strokeDashoffset: dashOffset
            }} />
      </svg>
      <div className='clock'>
      <div className="hours-container">
        <div className="hours" style={hourStyles}></div>
      </div>
      <div className="minutes-container">
        <div className="minutes" id="minute" style={minuteStyles}></div>
      </div>
      </div>
      </Fragment>
    }
      </div>
    );
    // } else {
    // return (
    //   <Fragment>
    //   <div className='article-progress-track'>
    //     <div className='article-progress-bar' style={progressBarStyles}></div>
    //   </div>
    //   {(this.state.percentage >= 100) &&
    //     <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
    //       <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
    //       <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
    //     </svg>
    //   }
    //   </Fragment>
    // );
    // }
  }
}

export default ArticleProgress;

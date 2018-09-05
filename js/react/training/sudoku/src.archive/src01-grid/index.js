import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import _ from 'lodash';

class Square extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      class: "square"
    };
  }

  render() {
    if (this.props.col > 0 && this.props.col % 3 == 0) this.state.class += " left";
    if (this.props.row > 0 && this.props.row % 3 == 0) this.state.class += " top";
    return (
      <button
        className={this.state.class}
        onClick={() => this.setState({
          value: this.state.value < 9 ? this.state.value + 1 : 1
        })}
      >
        {this.state.value}
      </button>
    );
    /* to display coordinates use these instead of {this.state.value}
        {this.props.row},{this.props.col}
    */
  }
}

class Board extends React.Component {
  renderSquare(i, j) {
    return <Square row={i} col={j} value="0" />;
  }

  render() {
    const s = 9;
    return (
      <div>
        {_.times(s, r =>
          <div className="board-row">
            {_.times(s, c =>
              this.renderSquare(r,c)
            )}
          </div>
        )}
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

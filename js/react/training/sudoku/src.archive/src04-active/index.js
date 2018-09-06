import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import _ from 'lodash';

const s = 9;

function Circle(props) {
  return (
    <button
      className={props.active === props.value ? "circle active" : "circle"}
      onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Choice extends React.Component {
  renderCircle(i) {
    return (
      <Circle
        value={i}
        active={this.props.active}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        {_.times(s, i =>
          this.renderCircle(i+1)
        )}
      </div>
    );
  }
}

function Square(props) {
  return (
    <button
      className={props.class + " left" + props.col + " top" + props.row}
      onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(r, c) {
    return (
      <Square
        key={"square" + r + c}
        row={r} col={c} class="square"
        value={this.props.squares[s*r+c]}
        onClick={() => this.props.onClick(r, c)}
      />
    );
  }

  render() {
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
  constructor(props) {
    super(props);
    this.state = {
      circle: 1,
      squares: Array(9*9).fill(null)
    };
  }

  handleClickCircle(i) {
    this.setState({
      circle: i
    })
  }

  handleClickSquare(r, c) {
    const circle = this.state.circle;
    const squares = this.state.squares.slice();
    squares[s*r+c] = (squares[s*r+c] !== circle) ? circle : null;
    this.setState({
      squares: squares
    });
  }

  render() {
    const circle = this.state.circle;
    const squares = this.state.squares;
    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={squares}
            onClick={(r, c) => this.handleClickSquare(r, c)}
          />
        </div>
        <div className="game-nums">
          <Choice
            active={circle}
            onClick={(i) => this.handleClickCircle(i)}
          />
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

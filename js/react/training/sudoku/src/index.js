import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import _ from 'lodash';

const s = 9;

function Circle(props) {
  return (
    <button
      count={props.count[props.value]}
      className={
        "circle" +
        (props.count[props.value] >= s ? " filled" : "") +
        (props.active === props.value ? " active" : "")
      }
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
        count={this.props.count}
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
      className={
        props.class +
        " top" + props.row +
        " left" + props.col +
        (props.bad ? " red" : "")
      }
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
        bad={this.props.squares[s*r+c] < 0}
        row={r} col={c} class="square"
        value={Math.abs(this.props.squares[s*r+c]).toString().replace('0', '')}
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
      circles: {},
      squares: Array(s*s).fill(null)
    };
  }

  handleClickCircle(i) {
    this.setState({
      circle: i
    })
  }

  handleClickSquare(r, c) {
    //alert(JSON.stringify(this.state.circles));
    const circle = this.state.circle;
    const squares = this.state.squares.slice();
    squares[s*r+c] = checkConflicts(r, c, squares, circle);
    let circles = _.countBy(squares, Math.floor);
    this.setState({
      circles: circles,
      squares: squares
    });
  }
;
  render() {
    const circle = this.state.circle;
    const circles = this.state.circles;
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
            count={circles}
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

function checkConflicts(r, c, squares, circle) {
  let check = circle; //(circle === 1) ? -1 : circle;
  return (squares[s*r+c] !== circle) ? check : null;
}

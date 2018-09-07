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
    const circle = this.state.circle;
    let squares = this.state.squares.slice();
    squares[s*r+c] = (Math.abs(squares[s*r+c]) === circle) ? null : circle;
    let circles = _.countBy(squares, Math.floor);
    squares = revertSquares(squares.slice());
    this.setState({
      circles: circles,
      squares: squares[s*r+c] < 1 ? squares : checkConflicts(r, c, squares, circle)
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

// operational complexity? 3 * O(s)
function checkConflicts(r, c, squares, circle) {
  let conflict = false;
  for (let i = 0; i < s; i++) {
    // Horizontal check
    if (i !== c && Math.abs(squares[s*r+i]) === circle) {
      squares[s*r+i] = squares[s*r+c] = -circle;
      conflict = true;
    }

    // Vertical check
    if (i !== r && Math.abs(squares[s*i+c]) === circle) {
      squares[s*i+c] = squares[s*r+c] = -circle;
      conflict = true;
    }

    // Quadrant check
    let Q = 3*Math.floor(r/3) + Math.floor(c/3);
    let k = 9*Q - 6*(Q%3) + 6*Math.floor(i/3) + i
    if (i !== 3*(r%3) + (c%3) && Math.abs(squares[k]) === circle) {
      squares[k] = squares[s*r+c] = -circle;
      conflict = true;
    }
  }
  if (!conflict) squares[s*r+c] = circle;
  return squares;
}

function revertSquares(squares) {
    for (let r = 0; r < s; r++) {
      for (let c = 0; c < s; c++) {
        if (squares[s*r+c] < 0)
          squares = checkConflicts(r, c, squares, Math.abs(squares[s*r+c]));
      }
    }
    return squares;
}

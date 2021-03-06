import React from 'react';
import ReactDOM from 'react-dom';
import _ from 'lodash';
import './index.css';

//import { Router, Route, Link } from 'react-router';
//const query = new URLSearchParams(this.props.location.search); alert(query.get('input'));

const s = 9;

function Input(props) {
  return (
    <form className="input" onSubmit={props.onSubmit}>
      <label>
        <input className="entry" type="text" value={props.value} onChange={props.onChange} />
      </label>
      <input className="submit" type="submit" value="LOAD" />
    </form>
  );
}

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
        key={"choice" + i}
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
        (props.bad ? " red" : "") +
        (props.lock ? " green": "")
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
        row={r} col={c} class="square"
        bad={this.props.squares[s*r+c] < 0}
        lock={this.props.locked[s*r+c] > 0}
        value={Math.abs(this.props.squares[s*r+c]).toString().replace('0', '')}
        onClick={() => this.props.onClick(r, c)}
      />
    );
  }

  render() {
    return (
      <div>
        {_.times(s, r =>
          <div className={"board-row row" + r}>
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
      input: '600120384008459072000006005000264030070080006940003000310000050089700000502000190',
      circle: 1,
      circles: {},
      squares: Array(s*s).fill(null),
      locked: Array(s*s).fill(null)
    };
  }

  handleChange(event) {
    this.setState({input: event.target.value});
  }

  handleSubmit(event) {
    let values = this.state.input.replace(/[^\d]+/g, '');
    this.setState({
      locked: values.split(''),
      squares: values.split('')
    });
    event.preventDefault();
  }

  handleClickCircle(i) {
    this.setState({
      circle: i
    })
  }

  handleClickSquare(r, c) {
    if (this.state.locked[s*r+c] > 0) return;
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

  render() {
    const input = this.state.input;
    const locked = this.state.locked;
    const circle = this.state.circle;
    const circles = this.state.circles;
    const squares = this.state.squares;
    return (
      <div className="game">
        <div className="game-board">
          <Board
            locked={locked}
            squares={squares}
            onClick={(r, c) => this.handleClickSquare(r, c)}
          />
          <Input
            value={input}
            onChange={(e) => this.handleChange(e)}
            onSubmit={(e) => this.handleSubmit(e)}
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

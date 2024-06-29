const canvas = document.getElementById('mainCanvas');
const ctx = canvas.getContext('2d');

const WHITE   = 'rgb(255, 255, 255)';
const BLACK   = 'rgb(0, 0, 0)';
const RED     = 'rgb(255, 0, 0)';
const GREEN   = 'rgb(0, 255, 0)';
const BLUE    = 'rgb(0, 0, 255)';
const CYAN    = 'rgb(0, 255, 255)';
const MAGENTA = 'rgb(255, 0, 255)';
const YELLOW  = 'rgb(255, 255, 0)';

const pi = Math.PI;

let x1 = -163.046875;
let x2 = -283.28125;
let x3 = 410;
let x4 = 300;
let a_of_turn = 0.25;

const screen_width = 1024;
const plot_frac = screen_width / (2 * pi);
const test_steps_per_dim = 120;
const test_circle_width = screen_width / test_steps_per_dim;

let view_test_grid = true;
const a_pos = { x: 350, y: 500 };

const plot_points = 100;
const test_angles = 100;
const test_tol = 1;

function lerp(x0, x1, t) {
    return x0 * (1 - t) + x1 * t;
}

function unlerp(x0, x1, t) {
    return (t - x0) / (x1 - x0);
}

function sqr_distance(v0, v1) {
    return (v1.x - v0.x) ** 2 + (v1.y - v0.y) ** 2;
}

function get_b_angles_1(a, x1, x2, x3, x4) {
    const y_discriminant = x1 ** 2 + x4 ** 2 - 2 * x1 * x4 * Math.cos(a);
    if (y_discriminant > 0) {
        const y = Math.sqrt(y_discriminant);
        const b1_arg = (x1 / y) * Math.sin(a);
        if (b1_arg >= -1 && b1_arg <= 1) {
            const b1 = Math.asin(b1_arg);
            const denom = 2 * x2 * y;
            if (denom !== 0) {
                const b2_arg = (x2 ** 2 + y ** 2 - x3 ** 2) / denom;
                if (b2_arg >= -1 && b2_arg <= 1) {
                    const b2 = Math.acos(b2_arg);
                    const b_plus = b1 + b2;
                    const b_minus = b1 - b2;
                    return [b_plus, b_minus];
                }
            }
        }
    }
    return null;
}

function get_b_angles_2(a, x1, x2, x3, x4) {
    const y_discriminant = x1 ** 2 + x4 ** 2 - 2 * x1 * x4 * Math.cos(a);
    if (y_discriminant > 0) {
        let y = Math.sqrt(y_discriminant);
        if (a > pi) y = -y;
        const denom1 = 2 * x4 * y;
        if (denom1 !== 0) {
            const b1_arg = (x4 ** 2 + y ** 2 - x1 ** 2) / denom1;
            if (b1_arg >= -1 && b1_arg <= 1) {
                const b1 = Math.acos(b1_arg);
                const denom2 = 2 * x2 * y;
                if (denom2 !== 0) {
                    const b2_arg = (x2 ** 2 + y ** 2 - x3 ** 2) / denom2;
                    if (b2_arg >= -1 && b2_arg <= 1) {
                        const b2 = Math.acos(b2_arg);
                        let b_plus = (b1 + b2 + pi) % (2 * pi) - pi;
                        let b_minus = (b1 - b2 + pi) % (2 * pi) - pi;
                        return a > pi ? [b_plus, b_minus] : [b_minus, b_plus];
                    }
                }
            }
        }
    }
    return null;
}

function drawCircle(color, x, y, radius) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * pi);
    ctx.fill();
}

function drawLine(color, x1, y1, x2, y2) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

function draw() {
    ctx.fillStyle = BLACK;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (view_test_grid && x4 !== 0) {
        for (let test_x1_it = 0; test_x1_it <= test_steps_per_dim; test_x1_it++) {
            for (let test_x2_it = 0; test_x2_it <= test_steps_per_dim; test_x2_it++) {
                const test_x1_frac = test_x1_it / (test_steps_per_dim + 1);
                const test_x1 = lerp(-500, 500, test_x1_frac);

                const test_x2_frac = test_x2_it / (test_steps_per_dim + 1);
                const test_x2 = lerp(-500, 500, test_x2_frac);

                let angles_were_given = false;
                let constraint_breaking_found = false;
                for (let test_a_it = 0; test_a_it < test_angles; test_a_it++) {
                    const test_a = lerp(0, 2 * pi, test_a_it / test_angles);
                    const b_angles = get_b_angles_1(test_a, test_x1, test_x2, x3, x4);
                    if (b_angles) {
                        angles_were_given = true;
                        const [b_plus, b_minus] = b_angles;

                        const b_pos = { x: a_pos.x + x4, y: a_pos.y };
                        const a = 2 * pi * a_of_turn;
                        const c_pos = {
                            x: a_pos.x + x1 * Math.cos(a),
                            y: a_pos.y + x1 * Math.sin(a)
                        };

                        const d_plus_pos = {
                            x: b_pos.x + x2 * Math.cos(pi - b_plus),
                            y: b_pos.y + x2 * Math.sin(pi - b_plus)
                        };
                        const d_minus_pos = {
                            x: b_pos.x + x2 * Math.cos(pi - b_minus),
                            y: b_pos.y + x2 * Math.sin(pi - b_minus)
                        };

                        const cdplus_sqr_dist = sqr_distance(c_pos, d_plus_pos);
                        const cdminus_sqr_dist = sqr_distance(c_pos, d_minus_pos);

                        if (Math.abs(cdplus_sqr_dist - x3 ** 2) > test_tol || Math.abs(cdminus_sqr_dist - x3 ** 2) > test_tol) {
                            constraint_breaking_found = true;
                            break;
                        }
                    }
                }

                const color = constraint_breaking_found && angles_were_given ? RED : GREEN;
                drawCircle(color, lerp(0, screen_width, test_x1_frac), lerp(0, screen_width, test_x2_frac), test_circle_width);
            }
        }
    } else {
        for (let plot_a_it = 0; plot_a_it < plot_points; plot_a_it++) {
            const plot_a = lerp(0, 2 * pi, plot_a_it / plot_points);
            const b_angles = get_b_angles_1(plot_a, x1, x2, x3, x4);
            if (b_angles) {
                const [b_plus, b_minus] = b_angles;

                const a_in_screenspace = Math.round(plot_a * plot_frac);
                const b_plus_in_screenspace = Math.round(b_plus * plot_frac + screen_width / 2);
                const b_minus_in_screenspace = Math.round(b_minus * plot_frac + screen_width / 2);

                drawCircle(GREEN, a_in_screenspace, b_plus_in_screenspace, 5);
                drawCircle(GREEN, a_in_screenspace, b_minus_in_screenspace, 5);
            }
        }

        const b_pos = { x: a_pos.x + x4, y: a_pos.y };
        const a = 2 * pi * a_of_turn;
        const c_pos = {
            x: a_pos.x + x1 * Math.cos(a),
            y: a_pos.y + x1 * Math.sin(a)
        };

        drawLine(BLUE, a_of_turn * screen_width, 0, a_of_turn * screen_width, screen_width);

        const b_angles = get_b_angles_1(a, x1, x2, x3, x4);
        if (b_angles) {
            const [b_plus, b_minus] = b_angles;
            const d_plus_pos = {
                x: b_pos.x + x2 * Math.cos(pi - b_plus),
                y: b_pos.y + x2 * Math.sin(pi - b_plus)
            };
            const d_minus_pos = {
                x: b_pos.x + x2 * Math.cos(pi - b_minus),
                y: b_pos.y + x2 * Math.sin(pi - b_minus)
            };

            drawLine(RED, b_pos.x, b_pos.y, d_plus_pos.x, d_plus_pos.y);
            drawLine(CYAN, c_pos.x, c_pos.y, d_plus_pos.x, d_plus_pos.y);
            drawLine(WHITE, b_pos.x, b_pos.y, d_minus_pos.x, d_minus_pos.y);
            drawLine(MAGENTA, c_pos.x, c_pos.y, d_minus_pos.x, d_minus_pos.y);
        }

        drawLine(GREEN, a_pos.x, a_pos.y, b_pos.x, b_pos.y);
        drawLine(YELLOW, a_pos.x, a_pos.y, c_pos.x, c_pos.y);
    }
}

function update() {
    a_of_turn += 0.001;
    a_of_turn %= 1;
    draw();
}

setInterval(update, 10);

window.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'q':
            x1 += 10;
            console.log("increase x1", x1, x2, x3, x4);
            draw();
            break;
        case 'a':
            x1 -= 10;
            console.log("decrease x1", x1, x2, x3, x4);
            draw();
            break;
        case 'w':
            x2 += 10;
            console.log("increase x2", x1, x2, x3, x4);
            draw();
            break;
        case 's':
            x2 -= 10;
            console.log("decrease x2", x1, x2, x3, x4);
            draw();
            break;
        case 'e':
            x3 += 10;
            console.log("increase x3", x1, x2, x3, x4);
            draw();
            break;
        case 'd':
            x3 -= 10;
            console.log("decrease x3", x1, x2, x3, x4);
            draw();
            break;
        case 'r':
            x4 += 10;
            console.log("increase x4", x1, x2, x3, x4);
            draw();
            break;
        case 'f':
            x4 -= 10;
            console.log("decrease x4", x1, x2, x3, x4);
            draw();
            break;
        case 't':
            view_test_grid = true;
            console.log("view_test_grid on");
            draw();
            break;
        case 'g':
            view_test_grid = false;
            console.log("view_test_grid off");
            draw();
            break;
    }
});

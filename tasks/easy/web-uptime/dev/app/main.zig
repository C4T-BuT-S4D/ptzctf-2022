const std = @import("std");
const web = @import("./lib/web.zig");
const graceful = @import("./lib/graceful.zig");

pub const io_mode = .evented;
pub const middleware = web.middleware;
pub const routes = web.routes;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    var server = web.Server.init(gpa.allocator());

    _ = async server.run();
    try graceful.run();
}

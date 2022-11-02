const std = @import("std");
const web = @import("./lib/web.zig");
const graceful = @import("./lib/graceful.zig");

pub const io_mode = .evented;
pub const middleware = web.middleware;
pub const routes = web.routes;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    var server = try web.Server.init(gpa.allocator(), "0.0.0.0:80");

    // Sleep to allow prometheus to try collecting our metrics.
    std.time.sleep(30 * std.time.ns_per_s);

    _ = async server.run();
    _ = async uptimeTest();

    try graceful.run();
}

// uptimeTest randomly shuts down our app to test the uptime functionalit
fn uptimeTest() void {
    var rnd = std.rand.DefaultPrng.init(@bitCast(u64, std.time.milliTimestamp()));
    const timeout = 30 + rnd.random().uintAtMost(u64, 30);
    std.log.err("crashing in {}s", .{timeout});
    std.time.sleep(timeout * std.time.ns_per_s);
    std.os.exit(42);
}

#!/usr/bin/env ruby
# Uses ordinary Bundler; an optional checkout-local Ruby development hook is
# supported on machines where development headers were extracted without sudo.
root = File.expand_path("..", __dir__)
hook = File.join(root, ".bundle", "ruby-headers.rb")
if File.file?(hook)
  require hook
  ENV["RUBYOPT"] = [ENV["RUBYOPT"], "-r#{hook}"].compact.join(" ")
end
ENV["BUNDLE_GEMFILE"] = File.join(root, "Gemfile")
Dir.chdir(root)
require "bundler/setup"
load Gem.bin_path("jekyll", "jekyll")

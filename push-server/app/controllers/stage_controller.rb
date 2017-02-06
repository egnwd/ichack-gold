class StageController < ApplicationController
  def done()
    ActionCable.server.broadcast "stages", message: params
  end
end

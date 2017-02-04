class StagesChannel < ApplicationCable::Channel
  def subscribed
    stream_from "stages"
  end

  def unsubscribed
    # Any cleanup needed when channel is unsubscribed
  end

end

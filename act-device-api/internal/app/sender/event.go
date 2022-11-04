package sender

import (
	"github.com/Shopify/sarama"
	"github.com/ozonmp/act-device-api/internal/model"
	"google.golang.org/protobuf/proto"

	pb "github.com/ozonmp/act-device-api/pkg/act-device-api"
	tspb "google.golang.org/protobuf/types/known/timestamppb"
)

//go:generate mockgen -source=./event.go -destination=./../../mocks/sender_mock.go -package=mocks
type EventSender interface {
	Send(event *model.DeviceEvent) error
}

type Sender struct {
	producer sarama.SyncProducer
	topic    string
}

func (s *Sender) Send(event *model.DeviceEvent) error {
	var payload *pb.Device

	if event.Device != nil {
		payload = &pb.Device{
			Id:        event.Device.ID,
			Platform:  event.Device.Platform,
			UserId:    event.Device.UserID,
			EnteredAt: tspb.New(*event.Device.EnteredAt),
		}
	}

	pbDeviceEvent := &pb.DeviceEvent{
		Id:       event.ID,
		DeviceId: event.DeviceId,
		Type:     uint64(event.Type),
		Status:   uint64(event.Status),
		Payload:  payload,
	}

	msgValue, err := proto.Marshal(pbDeviceEvent)

	if err != nil {
		return err
	}

	_, _, err = s.producer.SendMessage(&sarama.ProducerMessage{
		Topic:     s.topic,
		Value:     sarama.ByteEncoder(msgValue),
		Partition: -1,
	})

	return err
}

func NewEventSender(brokers []string, topic string) (*Sender, error) {
	config := sarama.NewConfig()
	config.Producer.Partitioner = sarama.NewRandomPartitioner
	config.Producer.RequiredAcks = sarama.WaitForAll
	config.Producer.Return.Successes = true
	producer, err := sarama.NewSyncProducer(brokers, config)

	sender := Sender{
		producer: producer,
		topic:    topic,
	}

	return &sender, err
}

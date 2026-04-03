package sensors

/*
#cgo LDFLAGS: -framework CoreGraphics
#include <CoreGraphics/CoreGraphics.h>
*/
import "C"

import (
	"sync"
	"time"

	"github.com/dinakars777/moody/mood"
)

// Display detects connection of external monitors
type Display struct {
	mu      sync.Mutex
	running bool
	stopCh  chan struct{}
}

func NewDisplay() *Display {
	return &Display{
		stopCh: make(chan struct{}),
	}
}

func (d *Display) Name() string { return "Display (External Monitor)" }

func (d *Display) Available() bool {
	return true
}

func (d *Display) Start(events chan<- mood.HardwareEvent) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	if d.running {
		return nil
	}
	d.running = true

	go d.pollLoop(events)
	return nil
}

func (d *Display) Stop() {
	d.mu.Lock()
	defer d.mu.Unlock()

	if d.running {
		close(d.stopCh)
		d.running = false
	}
}

func (d *Display) pollLoop(events chan<- mood.HardwareEvent) {
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	lastCount := d.getDisplayCount()

	for {
		select {
		case <-d.stopCh:
			return
		case <-ticker.C:
			count := d.getDisplayCount()
			if count > lastCount {
				events <- mood.HardwareEvent{
					Type:      mood.EventDisplayIn,
					Intensity: 0.5,
					Timestamp: time.Now(),
					Meta:      "Connected",
				}
			} else if count < lastCount {
				events <- mood.HardwareEvent{
					Type:      mood.EventDisplayOut,
					Intensity: 0.5,
					Timestamp: time.Now(),
					Meta:      "Disconnected",
				}
			}
			lastCount = count
		}
	}
}

func (d *Display) getDisplayCount() uint32 {
	var count C.uint32_t
	// Passing 0 limits to max capacity 0 to just write 'count'
	C.CGGetActiveDisplayList(0, nil, &count)
	return uint32(count)
}
